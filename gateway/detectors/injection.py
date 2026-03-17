"""
Prompt Injection and Jailbreak Detection Module
Author: Iqra Mushtaq
"""

import re
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


class InjectionDetector:
    """
    Detects prompt injection and jailbreak attempts using heuristic scoring
    """
    
    def __init__(self, config: dict):
        """
        Initialize the injection detector
        
        Args:
            config: Configuration dictionary with patterns and weights
        """
        self.config = config
        self.patterns = self._compile_patterns()
        self.weights = config.get('patterns', {})
        
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile regex patterns for detection"""
        patterns = {
            'instruction_override': [
                re.compile(r'ignore (previous|above|all) (instructions?|prompts?)', re.I),
                re.compile(r'forget (previous|above) (instructions?|prompts?)', re.I),
                re.compile(r'disregard (previous) (instructions?)', re.I),
                re.compile(r'do not follow (the )?(instructions?|prompts?)', re.I),
                re.compile(r'override (the )?(instructions?|prompts?)', re.I),
            ],
            'system_extraction': [
                re.compile(r'(system|initial) (prompt|instructions?)', re.I),
                re.compile(r'what (are|is) your (instructions?|prompts?)', re.I),
                re.compile(r'(show|display|print|output) your (prompt|instructions?)', re.I),
                re.compile(r'reveal (your|the) (system|hidden) (prompt|instructions?)', re.I),
            ],
            'jailbreak': [
                re.compile(r'\bDAN\b', re.I),
                re.compile(r'jail\s*break', re.I),
                re.compile(r'do anything now', re.I),
                re.compile(r'no (restrictions?|limits?|rules?)', re.I),
                re.compile(r'bypass (restrictions?|filters?|safety)', re.I),
            ],
            'special_chars': [
                re.compile(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]{10,}'),
                re.compile(r'\\[nrt]'),
            ]
        }
        return patterns
    
    def analyze(self, text: str) -> Tuple[float, Dict[str, float]]:
        """
        Analyze text for injection attempts
        
        Returns:
            Tuple of (total_score, details_dict)
        """
        if not text or not text.strip():
            return 0.0, {}
        
        scores = {}
        
        for category, patterns in self.patterns.items():
            category_score = 0.0
            
            for pattern in patterns:
                found = pattern.findall(text)
                if found:
                    category_score += min(len(found) * 0.15, 0.6)
            
            weight = self.weights.get(category, 0.3)
            if category_score > 0:
                scores[category] = min(category_score * weight, 1.0)
        
        total_score = min(sum(scores.values()), 1.0)
        return total_score, scores
    
    def get_risk_level(self, score: float) -> str:
        """Convert numerical score to risk level"""
        if score >= 0.7:
            return "CRITICAL"
        elif score >= 0.5:
            return "HIGH"
        elif score >= 0.3:
            return "MEDIUM"
        elif score >= 0.1:
            return "LOW"
        else:
            return "NONE"