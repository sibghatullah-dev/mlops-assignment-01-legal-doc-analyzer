#!/bin/bash

# Model Setup Script for Legal Document Analyzer
# This script handles the setup of the pre-trained model files

echo "🤖 Legal Document Analyzer - Model Setup"
echo "========================================="

MODEL_DIR="app/model"
MODEL_FILE="$MODEL_DIR/model.safetensors"

# Create model directory if it doesn't exist
mkdir -p "$MODEL_DIR"

if [ -f "$MODEL_FILE" ]; then
    echo "✅ Model file already exists: $MODEL_FILE"
    echo "📊 File size: $(du -h "$MODEL_FILE" | cut -f1)"
else
    echo "❌ Model file not found: $MODEL_FILE"
    echo ""
    echo "📋 To set up the model:"
    echo "1. Train the model using: python model/train.py"
    echo "2. Or copy your pre-trained model files to: $MODEL_DIR/"
    echo ""
    echo "📁 Required model files:"
    echo "   - config.json"
    echo "   - model.safetensors"
    echo "   - tokenizer.json"
    echo "   - tokenizer_config.json"
    echo "   - vocab.txt"
    echo "   - special_tokens_map.json"
    echo ""
    echo "⚠️  Note: model.safetensors is excluded from git due to large size"
    exit 1
fi

# Check other required model files
required_files=("config.json" "tokenizer.json" "tokenizer_config.json" "vocab.txt" "special_tokens_map.json")

echo ""
echo "🔍 Checking required model files:"
all_present=true

for file in "${required_files[@]}"; do
    if [ -f "$MODEL_DIR/$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        all_present=false
    fi
done

if [ "$all_present" = true ]; then
    echo ""
    echo "🎉 All model files are present!"
    echo "🚀 Ready to run the application!"
else
    echo ""
    echo "⚠️  Some model files are missing. Please ensure all files are in place."
    exit 1
fi