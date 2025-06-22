# tokenise.py
import json
from tokenizers import Tokenizer
from tokenizers.models import BPE, WordPiece, Unigram
from tokenizers.trainers import BpeTrainer, WordPieceTrainer, UnigramTrainer
from tokenizers.pre_tokenizers import Whitespace
from transformers import AutoTokenizer
from transformers.pipelines import pipeline
import sentencepiece as spm

def setup_tokenizers():
    """Setup different tokenization algorithms"""
    
    # For demonstration, we'll use pre-trained tokenizers
    # BPE tokenizer (using GPT-2's tokenizer as example)
    bpe_tokenizer = AutoTokenizer.from_pretrained("gpt2")
    
    # WordPiece tokenizer (using BERT's tokenizer)
    wordpiece_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    
    # SentencePiece Unigram (using T5's tokenizer)
    unigram_tokenizer = AutoTokenizer.from_pretrained("t5-small")
    
    return bpe_tokenizer, wordpiece_tokenizer, unigram_tokenizer

def tokenize_sentence(sentence):
    """Tokenize the given sentence with different algorithms"""
    
    bpe_tok, wp_tok, uni_tok = setup_tokenizers()
    
    results = {}
    
    # BPE Tokenization
    bpe_tokens = bpe_tok.tokenize(sentence)
    bpe_ids = bpe_tok.encode(sentence)
    results['BPE'] = {
        'tokens': bpe_tokens,
        'token_ids': bpe_ids,
        'count': len(bpe_tokens)
    }
    
    # WordPiece Tokenization  
    wp_tokens = wp_tok.tokenize(sentence)
    wp_ids = wp_tok.encode(sentence)
    results['WordPiece'] = {
        'tokens': wp_tokens,
        'token_ids': wp_ids,
        'count': len(wp_tokens)
    }
    
    # SentencePiece Unigram Tokenization
    uni_tokens = uni_tok.tokenize(sentence)
    uni_ids = uni_tok.encode(sentence)
    results['Unigram'] = {
        'tokens': uni_tokens,
        'token_ids': uni_ids,
        'count': len(uni_tokens)
    }
    
    return results


def mask_and_predict(sentence, tokenizer_name="bert-base-uncased"):
    """Mask tokens and predict using a language model"""
    
    # Use BERT for fill-mask task (7B models like Mistral aren't typically used for fill-mask)
    # For actual 7B model usage, you'd need significant computational resources
    
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    fill_mask = pipeline("fill-mask", model=tokenizer_name, tokenizer=tokenizer)
    
    # Create masked versions - replacing "cat" and "tired" with mask tokens
    masked_sentence1 = sentence.replace("cat", tokenizer.mask_token)
    masked_sentence2 = masked_sentence1.replace("tired", tokenizer.mask_token)
    
    print(f"Original: {sentence}")
    print(f"Masked: {masked_sentence2}")
    
    # Get predictions
    predictions = fill_mask(masked_sentence2)
    
    results = {
        'original_sentence': sentence,
        'masked_sentence': masked_sentence2,
        'predictions': predictions
    }
    
    return results

# Note: For actual 7B model usage like Mistral-7B-Instruct:
def use_large_model_prediction(sentence):
    """
    Example of how you would use a 7B model (requires significant resources)
    """
    # This would require substantial GPU memory
    # model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    
    # For demonstration purposes only - actual implementation would need:
    # - Proper prompt formatting for instruction models
    # - Adequate hardware resources
    # - Different approach since these aren't fill-mask models
    
    print("Note: 7B model usage requires significant computational resources")
    print("Using BERT for fill-mask demonstration instead")


if __name__ == "__main__":
    sentence = "The cat sat on the mat because it was tired."
    results = tokenize_sentence(sentence)
    data1 = mask_and_predict(sentence)
    data2 = use_large_model_prediction(sentence)
    
    # Print results
    for algorithm, data in results.items():
        print(f"\n{algorithm} Tokenization:")
        print(f"Tokens: {data['tokens']}")
        print(f"Token IDs: {data['token_ids']}")
        print(f"Total count: {data['count']}")

    print(f"Masked and Predicted: {data1}")
    print(f"Large Model Prediction: {data2}")
    
    # Save results
    with open('tokenization_results.json', 'w') as f:
        json.dump(results, f, indent=2)
