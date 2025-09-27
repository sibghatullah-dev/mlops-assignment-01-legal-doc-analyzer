# Model Files Directory - Google Drive Integration

This directory contains the fine-tuned LegalBERT model files for the Legal Document Analyzer.

## Model Files (Downloaded from Google Drive):
- `model.safetensors` (417.67 MB) - Fine-tuned LegalBERT weights  
- `tokenizer.json` (686 KB) - Tokenizer file
- `config.json` - Model configuration
- `tokenizer_config.json` - Tokenizer configuration
- `vocab.txt` - Vocabulary file
- `special_tokens_map.json` - Special tokens mapping

## Automatic Download

Large model files are automatically downloaded during Docker build from:
**Google Drive**: https://drive.google.com/file/d/1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg/view?usp=sharing

## Manual Setup

For local development, run:
```bash
./download_models.sh
```
- `special_tokens_map.json` - Special tokens mapping

## Setup:
1. Run the training script: `python model/train.py`
2. Or copy pre-trained model files to this directory
3. Use `./setup_model.sh` to verify all files are present

## Note:
The `model.safetensors` file is excluded from version control due to its large size (~400MB).
For production deployment, use external model storage or model registry services.