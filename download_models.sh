#!/bin/bash#!/bin/bash



echo "🤖 Legal Document Analyzer - Google Drive Model Download"echo "🤖 Legal Document Analyzer - Model Setup with Google Drive"

echo "======================================================="echo "=========================================================="



# Google Drive file ID for the model files# Configuration - REPLACE WITH YOUR ACTUAL GOOGLE DRIVE FILE ID

GOOGLE_DRIVE_FILE_ID="1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg"GOOGLE_DRIVE_FILE_ID="1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg"

MODEL_DIR="app/model"MODEL_DIR="app/model"

DOWNLOAD_URL="https://drive.google.com/uc?export=download&id=${GOOGLE_DRIVE_FILE_ID}"DOWNLOAD_URL="https://drive.google.com/uc?export=download&id=${GOOGLE_DRIVE_FILE_ID}"



# Create model directory# Create model directory if it doesn't exist

mkdir -p "$MODEL_DIR"mkdir -p "$MODEL_DIR"



echo "📥 Downloading model files from Google Drive..."echo "📥 Downloading model files from Google Drive..."

echo "File ID: $GOOGLE_DRIVE_FILE_ID"echo "File ID: $GOOGLE_DRIVE_FILE_ID"

echo "Destination: $MODEL_DIR"echo "Destination: $MODEL_DIR"

echoecho



# Check if already exists# Check if model files already exist

if [ -f "$MODEL_DIR/model.safetensors" ] && [ -f "$MODEL_DIR/tokenizer.json" ]; thenif [ -f "$MODEL_DIR/model.safetensors" ] && [ -f "$MODEL_DIR/tokenizer.json" ]; then

    echo "✅ Model files already exist!"    echo "✅ Model files already exist!"

    echo "📊 model.safetensors: $(du -h "$MODEL_DIR/model.safetensors" | cut -f1)"    echo "📊 model.safetensors: $(du -h "$MODEL_DIR/model.safetensors" | cut -f1)"

    echo "📊 tokenizer.json: $(du -h "$MODEL_DIR/tokenizer.json" | cut -f1)"    echo "📊 tokenizer.json: $(du -h "$MODEL_DIR/tokenizer.json" | cut -f1)"

    exit 0    echo "🐳 Ready to build Docker image!"

fi    exit 0

fi

# Download and extract

echo "⬇️  Starting download..."# Download model files

if wget --no-check-certificate "$DOWNLOAD_URL" -O model.zip; thenecho "⬇️  Starting download..."

    echo "✅ Download completed"if wget --no-check-certificate "$DOWNLOAD_URL" -O model.zip 2>/dev/null; then

        echo "✅ Download completed successfully"

    if unzip -q model.zip -d "$MODEL_DIR"; then    

        echo "✅ Model files extracted successfully"    echo "📦 Extracting model files..."

        rm model.zip    if unzip -q model.zip -d "$MODEL_DIR" 2>/dev/null; then

                echo "✅ Extraction completed successfully"

        echo "🔍 Verifying files..."        rm model.zip

        ls -la "$MODEL_DIR"        

                echo "🔍 Verifying model files..."

        echo "🎉 Setup complete! Ready for Docker build."        echo "Contents of $MODEL_DIR:"

    else        ls -la "$MODEL_DIR"

        echo "❌ Failed to extract files"        echo

        exit 1        

    fi        # Check critical files

else        CRITICAL_FILES=("model.safetensors" "tokenizer.json" "config.json")

    echo "❌ Download failed"        ALL_FOUND=true

    echo "💡 Please check the Google Drive link manually:"        

    echo "   https://drive.google.com/file/d/${GOOGLE_DRIVE_FILE_ID}/view"        for file in "${CRITICAL_FILES[@]}"; do

    exit 1            if [ -f "$MODEL_DIR/$file" ]; then

fi                echo "✅ $file found ($(du -h "$MODEL_DIR/$file" | cut -f1))"
            else
                echo "❌ $file NOT found"
                ALL_FOUND=false
            fi
        done
        
        echo
        if [ "$ALL_FOUND" = true ]; then
            echo "🎉 Model setup completed successfully!"
            echo "📁 Model files are ready in: $MODEL_DIR"
            echo "🐳 You can now build the Docker image:"
            echo "   docker build -t legal-doc-analyzer ."
            echo "🚀 Or run the container:"
            echo "   docker run -d --name legal-analyzer -p 5000:5000 legal-doc-analyzer"
        else
            echo "⚠️  Some model files are missing. Please check the Google Drive link."
        fi
        
    else
        echo "❌ Failed to extract model files"
        rm -f model.zip
        exit 1
    fi
else
    echo "❌ Failed to download model files"
    echo "💡 Please check:"
    echo "   1. Replace YOUR_FILE_ID_HERE with actual Google Drive file ID"
    echo "   2. Ensure Google Drive file is publicly accessible"
    echo "   3. Check internet connection"
    echo "   4. Manual download: https://drive.google.com/file/d/${GOOGLE_DRIVE_FILE_ID}/view"
    exit 1
fi