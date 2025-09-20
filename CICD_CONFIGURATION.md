# CI/CD Pipeline Configuration Guide

This document explains the configuration files for the Legal Document Analyzer CI/CD pipeline.

## 🏗️ Pipeline Architecture

The CI/CD pipeline follows this workflow:

```
dev branch → Code Quality Check (flake8) → test branch → Unit Testing → master branch → Jenkins Deployment
```

## 📁 Configuration Files

### 1. `.flake8` - Code Quality Configuration
- **Purpose**: Defines Python code quality standards
- **Trigger**: Runs on pushes/PRs to `dev` branch
- **Key Settings**:
  - Max line length: 120 characters
  - Max complexity: 10
  - Excludes cache and build directories
  - Ignores common formatting issues

### 2. GitHub Actions Workflows

#### `.github/workflows/lint.yml` - Code Quality Check
- **Trigger**: Push/PR to `dev` branch
- **Purpose**: Validates code quality using flake8
- **Features**:
  - Python 3.10 environment
  - Installs dependencies and flake8
  - Runs quality checks on app/, model/, tests/
  - Comments on PRs with results

#### `.github/workflows/test.yml` - Unit Testing
- **Trigger**: Push/PR to `test` branch
- **Purpose**: Runs automated unit tests
- **Features**:
  - Python 3.10 environment
  - Installs pytest and coverage tools
  - Runs tests with coverage reporting
  - Optional Codecov integration
  - Comments on PRs with test results

#### `.github/workflows/deploy.yml` - Production Deployment
- **Trigger**: Push to `master`/`main` branch or merged PR
- **Purpose**: Triggers Jenkins deployment job
- **Features**:
  - Securely triggers Jenkins using API
  - Uses GitHub secrets for authentication
  - Provides deployment status feedback

### 3. `Jenkinsfile` - Jenkins Pipeline Configuration
- **Trigger**: Only runs on `master`/`main` branch
- **Purpose**: Containerizes app and pushes to Docker Hub
- **Stages**:
  1. **Checkout**: Gets latest code and commit info
  2. **Pre-build Validation**: Validates repository state
  3. **Build Docker Image**: Creates Docker container
  4. **Push to DockerHub**: Uploads to registry
  5. **Deploy Notification**: Prepares deployment info
- **Email Notifications**:
  - Success: Sends detailed deployment info to admin
  - Failure: Sends error details with build links

### 4. `Dockerfile` - Container Configuration
- **Base Image**: Python 3.10-slim
- **Features**:
  - Installs system dependencies (gcc, g++)
  - Installs Python dependencies and gunicorn
  - Copies application code and model files
  - Creates non-root user for security
  - Exposes port 5000
  - Uses gunicorn with 2 workers

## 🔧 Required Jenkins Configuration

### Credentials Setup
You need to configure these credentials in Jenkins:

1. **docker-hub-credentials**: DockerHub username/password
2. **admin-email**: Administrator email address

### GitHub Secrets Setup
Configure these secrets in your GitHub repository:

1. **JENKINS_URL**: Your Jenkins server URL
2. **JENKINS_USER**: Jenkins username
3. **JENKINS_TOKEN**: Jenkins API token

## 🌊 Workflow Process

### Development Workflow
1. **Feature Development**: Create feature branch from `dev`
2. **Code Quality**: Push to `dev` → GitHub Actions runs flake8
3. **Testing**: Create PR from `dev` to `test` → GitHub Actions runs unit tests
4. **Production**: Create PR from `test` to `master` → Jenkins deployment triggers

### Admin Approval Process
- All changes require admin approval via pull requests
- Admin reviews code quality and test results
- Admin approves merge to next branch in sequence

### Notification System
- **Code Quality**: Comments on PRs with flake8 results
- **Unit Tests**: Comments on PRs with test results
- **Deployment**: Email notifications to admin with:
  - Build status (success/failure)
  - Docker image details
  - Commit information
  - Jenkins build links

## 🚀 Deployment Details

When code is merged to master:
1. GitHub Actions triggers Jenkins job
2. Jenkins builds Docker image
3. Image is pushed to Docker Hub
4. Admin receives email notification
5. Application is ready for production deployment

## 📋 Branch Protection Rules (Recommended)

Configure these branch protection rules in GitHub:

- **dev branch**: Require PR reviews, require status checks to pass
- **test branch**: Require PR reviews, require unit tests to pass
- **master branch**: Require PR reviews, require all checks to pass

## 🔍 Monitoring and Troubleshooting

- **Code Quality Issues**: Check GitHub Actions logs in lint workflow
- **Test Failures**: Check GitHub Actions logs in test workflow
- **Deployment Issues**: Check Jenkins build logs
- **Email Setup**: Ensure Jenkins email plugin is configured

## 🛠️ Local Development Setup

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run code quality check
flake8 --config .flake8 app/ model/ tests/

# Run unit tests
pytest tests/ -v

# Build Docker image locally
docker build -t legal-doc-analyzer .

# Run container locally
docker run -p 5000:5000 legal-doc-analyzer
```

This configuration ensures a robust CI/CD pipeline with proper code quality checks, automated testing, and secure deployment processes.