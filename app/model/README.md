# Model Files Directory

This directory contains the pre-trained model files for the Legal Document Analyzer.

## Required Files:
- `config.json` - Model configuration
- `model.safetensors` - Pre-trained model weights (excluded from git due to size)
- `tokenizer.json` - Tokenizer data
- `tokenizer_config.json` - Tokenizer configuration
- `vocab.txt` - Vocabulary file
- `special_tokens_map.json` - Special tokens mapping

## Setup:
1. Run the training script: `python model/train.py`
2. Or copy pre-trained model files to this directory
3. Use `./setup_model.sh` to verify all files are present

## Note:
The `model.safetensors` file is excluded from version control due to its large size (~400MB).
For production deployment, use external model storage or model registry services.