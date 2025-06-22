import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from validator import HallucinationValidator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LanguageModelSimulator:
    """Simulate a language model with predefined responses for testing."""
    
    def __init__(self):
        # Predefined responses - mix of correct, incorrect, and hallucinated answers
        self.responses = {
            "What is the capital of France?": ["London", "Paris"],  # Incorrect first, correct on retry
            "What is the largest planet in our solar system?": ["Saturn", "Jupiter"],
            "What is the chemical symbol for water?": ["H20", "H2O"],  # Typo first, correct on retry
            "Who wrote the novel '1984'?": ["Aldous Huxley", "George Orwell"],
            "What is the speed of light in vacuum?": ["300,000 km/s", "299,792,458 meters per second"],
            "What year did World War II end?": ["1944", "1945"],
            "What is the smallest unit of matter?": ["Molecule", "Atom"],
            "How many continents are there?": ["6", "7"],
            "What is the currency of Japan?": ["Yuan", "Yen"],
            "What is the boiling point of water at sea level?": ["212 degrees Fahrenheit", "100 degrees Celsius"],
            
            # Edge case questions (not in KB)
            "What is the population of Mars?": ["There is no permanent human population on Mars"],
            "What color is a unicorn?": ["Unicorns are mythical creatures and don't exist"],
            "How many moons does Earth have?": ["1"],
            "What is the capital of Atlantis?": ["Atlantis is a fictional place"],
            "What is 2+2?": ["4"]
        }
        self.attempt_count = {}
    
    def ask_question(self, question: str) -> str:
        """Simulate asking a question to the language model."""
        if question not in self.responses:
            return "I don't know the answer to that question."
        
        # Get attempt count for this question
        attempt = self.attempt_count.get(question, 0)
        responses = self.responses[question]
        
        # Use different response based on attempt
        if attempt < len(responses):
            response = responses[attempt]
        else:
            response = responses[-1]  # Use last response if out of attempts
            
        self.attempt_count[question] = attempt + 1
        return response


def run_hallucination_detection():
    """Main function to run the hallucination detection system."""
    logger.info("Starting hallucination detection system")
    
    # Initialize components
    validator = HallucinationValidator()
    model = LanguageModelSimulator()
    
    # Load knowledge base questions
    with open('kb.json', 'r') as f:
        kb_data = json.load(f)
    
    kb_questions = [item['question'] for item in kb_data['knowledge_base']]
    
    # Add edge case questions
    edge_questions = [
        "What is the population of Mars?",
        "What color is a unicorn?", 
        "How many moons does Earth have?",
        "What is the capital of Atlantis?",
        "What is 2+2?"
    ]
    
    all_questions = kb_questions + edge_questions
    
    results = []
    
    for question in all_questions:
        logger.info(f"Processing question: {question}")
        
        # First attempt
        answer = model.ask_question(question)
        logger.info(f"Model answer: {answer}")
        
        status, message = validator.validate_answer(question, answer)
        logger.info(f"Validation result: {status} - {message}")
        
        result = {
            "question": question,
            "first_answer": answer,
            "first_validation": {"status": status, "message": message},
            "retried": False,
            "final_status": status
        }
        
        # Retry if needed
        if status.startswith("RETRY"):
            logger.info(f"Retrying question: {question}")
            result["retried"] = True
            
            # Second attempt
            retry_answer = model.ask_question(question)
            logger.info(f"Retry answer: {retry_answer}")
            
            retry_status, retry_message = validator.validate_answer(question, retry_answer)
            logger.info(f"Retry validation: {retry_status} - {retry_message}")
            
            result["retry_answer"] = retry_answer
            result["retry_validation"] = {"status": retry_status, "message": retry_message}
            result["final_status"] = retry_status
        
        results.append(result)
        logger.info(f"Completed processing for: {question}\n")
    
    # Save results
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary
    generate_summary(results)
    
    logger.info("Hallucination detection system completed")
    return results


def generate_summary(results: List[Dict[str, Any]]):
    """Generate a summary of the validation results."""
    total_questions = len(results)
    kb_questions = sum(1 for r in results if r["first_validation"]["status"] != "RETRY_OUT_OF_DOMAIN")
    out_of_domain = sum(1 for r in results if r["first_validation"]["status"] == "RETRY_OUT_OF_DOMAIN")
    
    first_attempt_correct = sum(1 for r in results if r["first_validation"]["status"] == "VALID")
    retries_needed = sum(1 for r in results if r["retried"])
    
    final_correct = sum(1 for r in results if r["final_status"] == "VALID")
    final_incorrect = total_questions - final_correct
    
    summary_text = f"""# Hallucination Detection Summary

## Overview
- **Total Questions**: {total_questions}
- **KB Questions**: {kb_questions}
- **Out-of-Domain Questions**: {out_of_domain}

## First Attempt Results
- **Correct**: {first_attempt_correct}/{total_questions} ({first_attempt_correct/total_questions*100:.1f}%)
- **Retries Needed**: {retries_needed}/{total_questions} ({retries_needed/total_questions*100:.1f}%)

## Final Results (After Retries)
- **Correct**: {final_correct}/{total_questions} ({final_correct/total_questions*100:.1f}%)
- **Incorrect**: {final_incorrect}/{total_questions} ({final_incorrect/total_questions*100:.1f}%)

## Detailed Results

| Question | First Answer | Validation | Retried | Final Status |
|----------|-------------|------------|---------|-------------|
"""
    
    for result in results:
        question = result["question"][:50] + "..." if len(result["question"]) > 50 else result["question"]
        first_answer = result["first_answer"][:30] + "..." if len(result["first_answer"]) > 30 else result["first_answer"]
        validation = result["first_validation"]["status"]
        retried = "Yes" if result["retried"] else "No"
        final_status = result["final_status"]
        
        summary_text += f"| {question} | {first_answer} | {validation} | {retried} | {final_status} |\n"
    
    # Write summary to file
    with open('summary.md', 'w') as f:
        f.write(summary_text)
    
    logger.info("Summary generated and saved to summary.md")


if __name__ == "__main__":
    try:
        results = run_hallucination_detection()
        print("Hallucination detection completed successfully!")
        print("Check run.log for detailed logs and summary.md for results summary.")
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        raise
