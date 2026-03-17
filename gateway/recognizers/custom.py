"""
Custom Presidio Recognizers for PII Detection
Author: Iqra Mushtaq
"""

import re
from typing import List, Dict, Optional, Any
import logging

# We'll use mock mode since Presidio might not be installed
logger = logging.getLogger(__name__)


class MockPresidioAnalyzer:
    """Mock Presidio analyzer for testing"""
    
    def __init__(self):
        self.patterns = {
            'EMAIL_ADDRESS': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'PHONE_NUMBER': re.compile(r'\b(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'),
            'API_KEY': re.compile(r'\b[A-Za-z0-9-_]{20,40}\b'),
            'INTERNAL_ID': re.compile(r'\b(EMP|ID|CUST)[-_]?\d{6,8}\b', re.I),
        }
    
    def analyze(self, text: str) -> List[Dict]:
        """Analyze text for PII entities"""
        results = []
        
        for entity_type, pattern in self.patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                # Check if this is a false positive for API_KEY
                if entity_type == 'API_KEY':
                    # Skip if it looks like a regular word
                    if len(match.group()) < 20 and match.group().isalpha():
                        continue
                
                results.append({
                    'entity_type': entity_type,
                    'start': match.start(),
                    'end': match.end(),
                    'score': 0.85,
                    'text': match.group()
                })
        
        return results


class CustomPresidioAnalyzer:
    """
    Wrapper for Presidio Analyzer with custom recognizers
    """
    
    def __init__(self, config: dict):
        """
        Initialize with mock analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.min_score = config.get('min_score', 0.6)
        self.analyzer = MockPresidioAnalyzer()
        logger.info("Mock Presidio analyzer initialized")
    
    def analyze(self, text: str) -> List[Dict]:
        """
        Analyze text for PII entities
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected entities with metadata
        """
        try:
            results = self.analyzer.analyze(text)
            # Filter by minimum score
            return [r for r in results if r.get('score', 0) >= self.min_score]
        except Exception as e:
            logger.error(f"Error in PII analysis: {e}")
            return []