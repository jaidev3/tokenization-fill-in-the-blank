**compare.md:**
```markdown
# Tokenization Algorithm Comparison

## Key Differences

**BPE (Byte Pair Encoding):**
- Merges most frequent character pairs iteratively
- Good for handling out-of-vocabulary words
- Creates consistent subword boundaries

**WordPiece:**
- Maximizes likelihood of training data
- Uses ## prefix for subword continuations  
- Better for morphologically rich languages

**SentencePiece Unigram:**
- Uses unigram language model to determine splits
- Treats input as raw unicode characters
- More flexible boundary detection

The differences arise from their underlying algorithms and training objectives.