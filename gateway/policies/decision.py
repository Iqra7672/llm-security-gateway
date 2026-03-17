"""
Policy Decision Engine for Security Gateway
Author: Iqra Mushtaq
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class PolicyAction(Enum):
    """Possible policy actions"""
    ALLOW = "ALLOW"
    MASK = "MASK"
    BLOCK = "BLOCK"


@dataclass
class PolicyDecision:
    """Decision result from policy engine"""
    action: PolicyAction
    reason: str
    metadata: Dict[str, Any] = None


class PolicyEngine:
    """
    Policy decision engine for security gateway
    Decides whether to ALLOW, MASK, or BLOCK based on scores
    """
    
    def __init__(self, config: dict):
        """
        Initialize policy engine
        
        Args:
            config: Configuration dictionary with thresholds
        """
        self.config = config
        self.block_threshold = config.get('block_threshold', 0.7)
        self.mask_threshold = config.get('mask_threshold', 0.4)
        self.mask_entities = config.get('mask_entities', 
                                        ['PHONE_NUMBER', 'EMAIL_ADDRESS'])
        self.block_entities = config.get('block_entities',
                                         ['API_KEY'])
        
        logger.info(f"Policy Engine initialized: block={self.block_threshold}, "
                   f"mask={self.mask_threshold}")
    
    def decide(self, injection_score: float, pii_entities: List[Dict], 
               metadata: Optional[Dict] = None) -> PolicyDecision:
        """
        Make policy decision based on scores and entities
        
        Args:
            injection_score: Score from injection detection (0-1)
            pii_entities: List of detected PII entities
            metadata: Additional context for decision
            
        Returns:
            PolicyDecision with action and reason
        """
        # Check for high-risk PII that should be blocked
        for entity in pii_entities:
            if entity.get('entity_type') in self.block_entities:
                return PolicyDecision(
                    action=PolicyAction.BLOCK,
                    reason=f"Blocked due to high-risk PII: {entity.get('entity_type')}",
                    metadata={'entity': entity}
                )
        
        # Check injection score for blocking
        if injection_score >= self.block_threshold:
            return PolicyDecision(
                action=PolicyAction.BLOCK,
                reason=f"Injection score {injection_score:.2f} exceeds block threshold",
                metadata={'injection_score': injection_score}
            )
        
        # Check if masking is needed
        if pii_entities and injection_score < self.mask_threshold:
            # Only mask if injection score is low
            return PolicyDecision(
                action=PolicyAction.MASK,
                reason=f"Masking {len(pii_entities)} PII entities",
                metadata={'entities': pii_entities}
            )
        elif pii_entities and injection_score >= self.mask_threshold:
            # High injection + PII = block
            return PolicyDecision(
                action=PolicyAction.BLOCK,
                reason=f"Combined risk: injection {injection_score:.2f} and PII present",
                metadata={'injection_score': injection_score, 'pii_count': len(pii_entities)}
            )
        
        # Default: allow
        return PolicyDecision(
            action=PolicyAction.ALLOW,
            reason="No risks detected",
            metadata={'injection_score': injection_score}
        )