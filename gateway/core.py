"""
Core Security Gateway Implementation
Author: Iqra Mushtaq
"""

import re
import time
import yaml
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from .detectors.injection import InjectionDetector
from .recognizers.custom import CustomPresidioAnalyzer
from .policies.decision import PolicyEngine, PolicyDecision, PolicyAction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessingStage(Enum):
    """Processing stages for latency tracking"""
    INJECTION_DETECTION = "injection_detection"
    PII_ANALYSIS = "pii_analysis"
    POLICY_DECISION = "policy_decision"
    PII_MASKING = "pii_masking"
    TOTAL = "total"


@dataclass
class ProcessingResult:
    """Result of processing a user input"""
    original_input: str
    processed_input: Optional[str]
    injection_score: float
    injection_details: Dict[str, float]
    pii_entities: List[Dict]
    decision: PolicyDecision
    latency: Dict[str, float] = field(default_factory=dict)
    blocked: bool = False
    error: Optional[str] = None


class SecurityGateway:
    """
    Main Security Gateway for LLM Protection
    Implements pipeline: Input → Injection Detection → Presidio → Policy → Output
    """
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        """
        Initialize the security gateway with configuration
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.config = self._load_config(config_path)
        self.injection_detector = InjectionDetector(self.config.get('injection', {}))
        self.presidio_analyzer = CustomPresidioAnalyzer(self.config.get('presidio', {}))
        self.policy_engine = PolicyEngine(self.config.get('policy', {}))
        
        logger.info("Security Gateway initialized successfully")
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            'injection': {
                'threshold': 0.5,
                'patterns': {
                    'instruction_override': 0.4,
                    'system_extraction': 0.3,
                    'jailbreak': 0.5,
                    'special_chars': 0.2
                }
            },
            'presidio': {
                'entities': ['PHONE_NUMBER', 'API_KEY', 'INTERNAL_ID', 
                            'EMAIL_ADDRESS'],
                'min_score': 0.6
            },
            'policy': {
                'block_threshold': 0.7,
                'mask_threshold': 0.4,
                'mask_entities': ['PHONE_NUMBER', 'EMAIL_ADDRESS'],
                'block_entities': ['API_KEY']
            }
        }
    
    def process_input(self, user_input: str, metadata: Optional[Dict] = None) -> ProcessingResult:
        """
        Process user input through the security pipeline
        
        Args:
            user_input: Raw input string from user
            metadata: Additional metadata for processing
            
        Returns:
            ProcessingResult containing all processing information
        """
        latencies = {}
        start_time = time.time()
        
        try:
            # Stage 1: Injection Detection
            stage_start = time.time()
            injection_score, injection_details = self.injection_detector.analyze(user_input)
            latencies[ProcessingStage.INJECTION_DETECTION.value] = (time.time() - stage_start) * 1000
            
            # Stage 2: PII Analysis
            stage_start = time.time()
            pii_results = self.presidio_analyzer.analyze(user_input)
            latencies[ProcessingStage.PII_ANALYSIS.value] = (time.time() - stage_start) * 1000
            
            # Stage 3: Policy Decision
            stage_start = time.time()
            decision = self.policy_engine.decide(injection_score, pii_results, metadata)
            latencies[ProcessingStage.POLICY_DECISION.value] = (time.time() - stage_start) * 1000
            
            # Stage 4: Apply Decision
            processed_input = user_input
            blocked = False
            error = None
            
            if decision.action == PolicyAction.BLOCK:
                blocked = True
                error = f"Input blocked: {decision.reason}"
                logger.info(f"Blocked input: {decision.reason}")
                
            elif decision.action == PolicyAction.MASK:
                stage_start = time.time()
                processed_input = self._mask_pii(user_input, pii_results)
                latencies[ProcessingStage.PII_MASKING.value] = (time.time() - stage_start) * 1000
                logger.debug(f"Masked PII in input")
            
            # Total latency
            latencies[ProcessingStage.TOTAL.value] = (time.time() - start_time) * 1000
            
            return ProcessingResult(
                original_input=user_input,
                processed_input=processed_input if not blocked else None,
                injection_score=injection_score,
                injection_details=injection_details,
                pii_entities=pii_results,
                decision=decision,
                latency=latencies,
                blocked=blocked,
                error=error
            )
            
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            latencies[ProcessingStage.TOTAL.value] = (time.time() - start_time) * 1000
            return ProcessingResult(
                original_input=user_input,
                processed_input=None,
                injection_score=0.0,
                injection_details={},
                pii_entities=[],
                decision=PolicyDecision(action=PolicyAction.BLOCK, reason=f"Internal error: {str(e)}"),
                latency=latencies,
                blocked=True,
                error=str(e)
            )
    
    def _mask_pii(self, text: str, entities: List[Dict]) -> str:
        """Mask PII entities in the text"""
        masked_text = text
        for entity in sorted(entities, key=lambda x: len(x.get('text', '')), reverse=True):
            if 'text' in entity and entity['text']:
                entity_text = entity['text']
                entity_type = entity.get('entity_type', 'UNKNOWN')
                
                if entity_type == 'EMAIL_ADDRESS':
                    mask = '[EMAIL REDACTED]'
                elif entity_type == 'PHONE_NUMBER':
                    mask = '[PHONE REDACTED]'
                elif entity_type == 'API_KEY':
                    mask = '[API KEY REDACTED]'
                elif entity_type == 'INTERNAL_ID':
                    mask = '[ID REDACTED]'
                else:
                    mask = '[REDACTED]'
                
                masked_text = masked_text.replace(entity_text, mask)
        
        return masked_text
    
    def forward_to_llm(self, text: str) -> Dict:
        """
        Forward processed text to LLM (mock implementation)
        
        Args:
            text: Processed input text
            
        Returns:
            Mock LLM response
        """
        return {
            'status': 'success',
            'response': f"LLM Response to: {text[:50]}...",
            'model': 'mock-llm'
        }