import json
import re
from typing import Dict, List, Tuple, Optional


class HallucinationValidator:
    """Validator to detect hallucinations by comparing answers against a knowledge base."""
    
    def __init__(self, kb_path: str = "kb.json"):
        """Initialize validator with knowledge base."""
        self.kb_path = kb_path
        self.knowledge_base = self._load_kb()
        
    def _load_kb(self) -> Dict[str, str]:
        """Load knowledge base from JSON file."""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert to dict for easy lookup
                kb_dict = {}
                for item in data['knowledge_base']:
                    kb_dict[item['question'].strip().lower()] = item['answer'].strip()
                return kb_dict
        except FileNotFoundError:
            print(f"Knowledge base file {self.kb_path} not found!")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in {self.kb_path}!")
            return {}
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison (lowercase, remove extra spaces)."""
        return re.sub(r'\s+', ' ', text.strip().lower())
    
    def _is_answer_match(self, expected: str, actual: str) -> bool:
        """Check if actual answer matches expected answer using basic string matching."""
        expected_norm = self._normalize_text(expected)
        actual_norm = self._normalize_text(actual)
        
        # Exact match
        if expected_norm == actual_norm:
            return True
            
        # Check if expected answer is contained in actual answer
        if expected_norm in actual_norm:
            return True
            
        # Check if actual answer is contained in expected answer
        if actual_norm in expected_norm:
            return True
            
        return False
    
    def validate_answer(self, question: str, answer: str) -> Tuple[str, str]:
        """
        Validate an answer against the knowledge base.
        
        Returns:
            Tuple[str, str]: (status, message)
            - status: "VALID", "RETRY_MISMATCH", or "RETRY_OUT_OF_DOMAIN"
            - message: descriptive message
        """
        question_norm = self._normalize_text(question)
        
        # Check if question exists in KB
        expected_answer = None
        for kb_question, kb_answer in self.knowledge_base.items():
            if self._normalize_text(kb_question) == question_norm:
                expected_answer = kb_answer
                break
        
        if expected_answer is None:
            return "RETRY_OUT_OF_DOMAIN", "RETRY: out-of-domain"
        
        # Question is in KB, check if answer matches
        if self._is_answer_match(expected_answer, answer):
            return "VALID", "Answer matches knowledge base"
        else:
            return "RETRY_MISMATCH", "RETRY: answer differs from KB"
    
    def get_expected_answer(self, question: str) -> Optional[str]:
        """Get the expected answer for a question from the knowledge base."""
        question_norm = self._normalize_text(question)
        
        for kb_question, kb_answer in self.knowledge_base.items():
            if self._normalize_text(kb_question) == question_norm:
                return kb_answer
        return None
