# Hallucination Detection Summary

## Overview
- **Total Questions**: 15
- **KB Questions**: 10
- **Out-of-Domain Questions**: 5

## First Attempt Results
- **Correct**: 0/15 (0.0%)
- **Retries Needed**: 15/15 (100.0%)

## Final Results (After Retries)
- **Correct**: 10/15 (66.7%)
- **Incorrect**: 5/15 (33.3%)

## Detailed Results

| Question | First Answer | Validation | Retried | Final Status |
|----------|-------------|------------|---------|-------------|
| What is the capital of France? | London | RETRY_MISMATCH | Yes | VALID |
| What is the largest planet in our solar system? | Saturn | RETRY_MISMATCH | Yes | VALID |
| What is the chemical symbol for water? | H20 | RETRY_MISMATCH | Yes | VALID |
| Who wrote the novel '1984'? | Aldous Huxley | RETRY_MISMATCH | Yes | VALID |
| What is the speed of light in vacuum? | 300,000 km/s | RETRY_MISMATCH | Yes | VALID |
| What year did World War II end? | 1944 | RETRY_MISMATCH | Yes | VALID |
| What is the smallest unit of matter? | Molecule | RETRY_MISMATCH | Yes | VALID |
| How many continents are there? | 6 | RETRY_MISMATCH | Yes | VALID |
| What is the currency of Japan? | Yuan | RETRY_MISMATCH | Yes | VALID |
| What is the boiling point of water at sea level? | 212 degrees Fahrenheit | RETRY_MISMATCH | Yes | VALID |
| What is the population of Mars? | There is no permanent human po... | RETRY_OUT_OF_DOMAIN | Yes | RETRY_OUT_OF_DOMAIN |
| What color is a unicorn? | Unicorns are mythical creature... | RETRY_OUT_OF_DOMAIN | Yes | RETRY_OUT_OF_DOMAIN |
| How many moons does Earth have? | 1 | RETRY_OUT_OF_DOMAIN | Yes | RETRY_OUT_OF_DOMAIN |
| What is the capital of Atlantis? | Atlantis is a fictional place | RETRY_OUT_OF_DOMAIN | Yes | RETRY_OUT_OF_DOMAIN |
| What is 2+2? | 4 | RETRY_OUT_OF_DOMAIN | Yes | RETRY_OUT_OF_DOMAIN |
