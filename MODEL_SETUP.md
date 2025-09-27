# Model Setup Guide - Google Drive Integration# Model Setup Guide



## 🚀 Complete MLOps Solution with Google Drive Models## 🚀 Google Drive Integration



Due to GitHub's 100MB file size limit, the fine-tuned LegalBERT model files (417.67 MB) are hosted on Google Drive and automatically integrated into the Docker build process.Due to GitHub's 100MB file size limit, the fine-tuned LegalBERT model files (417.67 MB) are hosted on Google Drive and automatically downloaded during Docker build.



### 📥 Model Files Location### 📥 Model Files Location



**Google Drive Link**: [Download Model Files](https://drive.google.com/file/d/1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg/view?usp=sharing)**Google Drive Link**: [Download Model Files](https://drive.google.com/file/d/1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg/view?usp=sharing)



### 🐳 Automatic Docker Integration*(File ID: 1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg)*



The Dockerfile automatically downloads model files during build:### 🐳 Docker Automatic Setup



```dockerfileThe Dockerfile automatically downloads model files during build:

# Downloads model files from Google Drive during Docker build

RUN wget --no-check-certificate "https://drive.google.com/uc?export=download&id=1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg" -O model.zip && \```dockerfile

    unzip -q model.zip -d ./model/ && \# Downloads model files from Google Drive during build

    rm model.zipRUN wget --no-check-certificate "https://drive.google.com/uc?export=download&id=1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg" -O model.zip && \

```    unzip -q model.zip -d ./model/ && \

    rm model.zip

### 🔧 Manual Setup Options```



#### Option 1: Automatic Download Script### 🔧 Manual Setup Options

```bash

./download_models.sh#### Option 1: Automatic Download Script

``````bash

# Download and extract model files automatically

#### Option 2: Manual Download./download_models.sh

1. Download from Google Drive link above```

2. Extract to `app/model/` directory

#### Option 2: Manual Download

### 📁 Complete Model Structure1. Download `model.zip` from the Google Drive link above

2. Extract to `app/model/` directory:

``````bash

app/model/unzip model.zip -d app/model/

├── config.json                 # Model configuration (712 bytes)```

├── model.safetensors           # Fine-tuned LegalBERT weights (417.67 MB) ✅

├── tokenizer.json              # Tokenizer file (686 KB)  ## 📁 Complete Model Structure

├── tokenizer_config.json       # Tokenizer configuration (1.2 KB)

├── vocab.txt                   # Vocabulary file (217 KB)After download, your `app/model/` directory should contain:

├── special_tokens_map.json     # Special tokens mapping (125 bytes)

└── README.md                   # Model documentation```

```app/model/

├── config.json                 # Model configuration (712 bytes)

### 🚀 Quick Start├── model.safetensors           # Fine-tuned model weights (417.67 MB) 

├── tokenizer.json              # Tokenizer file (686 KB)

```bash├── tokenizer_config.json       # Tokenizer configuration (1.2 KB)

# Build Docker image (auto-downloads models)├── vocab.txt                   # Vocabulary file (217 KB)

docker build -t legal-doc-analyzer .├── special_tokens_map.json     # Special tokens mapping (125 bytes)

└── README.md                   # Model documentation

# Run container```

docker run -d --name legal-analyzer -p 5000:5000 legal-doc-analyzer

## 🐳 Docker Build Verification

# Test the application

curl http://localhost:5000/analyze -X POST \The application works correctly with the full model files:

  -H "Content-Type: application/json" \

  -d '{"text": "This agreement shall be governed by the laws of..."}'```bash

```# Build Docker image

docker build -t legal-doc-analyzer .

### ✅ Assignment Submission Ready

# Run container  

- ✅ Complete MLOps pipeline (GitHub Actions + Jenkins)docker run -d --name legal-analyzer -p 5000:5000 legal-doc-analyzer

- ✅ Docker containerization with automatic model download

- ✅ Clean GitHub repository (no large files)# Test the application

- ✅ Google Drive integration for model files  curl http://localhost:5000/analyze -X POST -H "Content-Type: application/json" \

- ✅ Fallback to mock model if download fails  -d '{"text": "This agreement shall be governed by the laws of..."}'

- ✅ All CI/CD workflows functional```



### 🔍 Verification## Model Loading Behavior



Check if models loaded successfully:1. **With Full Model**: Loads fine-tuned LegalBERT for accurate legal document analysis

```bash2. **Without Model Files**: Automatically falls back to mock model for testing

docker logs legal-analyzer

# Should show: "INFO:app:Model loaded successfully"## Assignment Submission Notes

# Not: "INFO:app:Using mock model for testing..."

```- ✅ Complete MLOps pipeline implemented

- ✅ CI/CD workflows (GitHub Actions + Jenkins)  

---- ✅ Docker containerization

- ✅ Model training scripts included

**Perfect for Assignment Submission**: Clean repository + Working Docker + Complete MLOps pipeline- ✅ Unit tests and code quality checks
- ⚠️ Large model files require local setup for full functionality

## Setup Instructions

1. Clone the repository
2. Download model files using the provided `setup_model.sh` script
3. Build and run Docker container
4. Access application at `http://localhost:5000`

---

**Note**: The mock model is used when large model files are not available, ensuring the application runs in all environments while demonstrating complete MLOps implementation.