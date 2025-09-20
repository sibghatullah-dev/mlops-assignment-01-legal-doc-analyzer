# AI-Based Legal Document Analyzer

This project analyzes legal contracts for risks, loopholes, and compliance issues using a fine-tuned LegalBERT model on the CUAD dataset. It includes a comprehensive CI/CD pipeline with GitHub Actions, Jenkins, and Docker.

## 🏗️ CI/CD Pipeline Architecture

The project implements a complete CI/CD pipeline with the following workflow:

```
dev branch → test branch → main/master branch
    ↓            ↓              ↓
 Lint Check  → Unit Tests → Docker Build & Deploy
 (flake8)    → (pytest)   → (Jenkins + Email)
```

### Pipeline Stages

1. **Development (dev branch)**
   - Code quality check with flake8
   - Admin approval required for merging

2. **Testing (test branch)**  
   - Automated unit testing with pytest
   - Integration testing verification
   - Admin approval required for merging

3. **Production (main branch)**
   - Jenkins job triggers automatically
   - Docker image build and push to DockerHub
   - Email notification to administrator

## 📁 Repository Structure

- **app/**: Contains the Flask API and its dependencies.
- **data/**: Instructions for downloading and using the CUAD dataset.
- **model/**: Scripts for fine-tuning LegalBERT on the CUAD dataset.
- **tests/**: Unit tests for the Flask API.
- **.github/workflows/**: GitHub Actions for linting, testing, and deployment.
- **Dockerfile**: Docker configuration to containerize the Flask app.
- **Jenkinsfile**: Jenkins pipeline definition for CI/CD.
- **BRANCH_PROTECTION_SETUP.md**: Complete guide for setting up branch protection rules.

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Docker
- Jenkins server
- DockerHub account
- GitHub repository with admin access

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/legal-doc-analyzer.git
   cd legal-doc-analyzer
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Download CUAD dataset:**
   - Follow instructions in `data/README.md`
   - Place `CUADv1.json` in the `data/` directory

5. **Train the model (optional):**
   ```bash
   cd model
   python train.py
   ```

6. **Run the application:**
   ```bash
   cd app
   python app.py
   ```

### CI/CD Pipeline Setup

#### 1. GitHub Repository Configuration

**Create Branches:**
```bash
git checkout -b dev
git push -u origin dev

git checkout -b test  
git push -u origin test
```

**Configure Branch Protection Rules:**
- Follow the detailed guide in `BRANCH_PROTECTION_SETUP.md`
- Ensure admin approval is required for all protected branches
- Set up required status checks for each branch

#### 2. GitHub Secrets Configuration

Add the following secrets in repository settings:

```
JENKINS_URL=https://your-jenkins-server.com
JENKINS_USER=your-jenkins-username
JENKINS_TOKEN=your-jenkins-api-token
```

#### 3. Jenkins Configuration

**Required Jenkins Plugins:**
- Pipeline
- Git
- Docker Pipeline
- Email Extension

**Jenkins Credentials:**
Create these credentials in Jenkins:
- `docker-hub-credentials`: DockerHub username/password
- `admin-email`: Administrator email address

**Jenkins Job Setup:**
1. Create new Pipeline job named `legal-doc-analyzer-deploy`
2. Configure Pipeline script from SCM
3. Point to your repository's Jenkinsfile
4. Set up webhook or polling for automatic triggers

#### 4. DockerHub Setup

1. Create DockerHub repository: `yourusername/legal-doc-analyzer`
2. Generate access token for Jenkins authentication

### Email Configuration

Configure Jenkins email settings:
1. Go to Manage Jenkins → Configure System
2. Set up SMTP server settings
3. Test email configuration

## 🔄 Development Workflow

### Feature Development Process

1. **Create Feature Branch:**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/your-feature-name
   ```

2. **Develop and Test Locally:**
   ```bash
   # Make your changes
   flake8 app/app.py --max-line-length=100  # Check code quality
   python -m pytest tests/ -v               # Run tests
   ```

3. **Push and Create PR to dev:**
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```
   - Create PR from `feature/your-feature-name` → `dev`
   - GitHub Actions runs flake8 linting
   - Admin reviews and approves
   - Merge to `dev`

4. **Integration Testing:**
   - Create PR from `dev` → `test`
   - GitHub Actions runs unit tests
   - Admin reviews and approves
   - Merge to `test`

5. **Production Deployment:**
   - Create PR from `test` → `main`
   - Admin reviews and approves  
   - Merge to `main` triggers:
     - GitHub Actions deployment workflow
     - Jenkins Docker build and push
     - Email notification to admin

## 🧪 Testing

### Running Tests Locally
```bash
# Install test dependencies
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_app.py::TestLegalDocAnalyzer::test_analyze_endpoint -v
```

### Code Quality Check
```bash
# Run flake8 linting
flake8 app/app.py --count --max-line-length=100 --statistics
```

## 🐳 Docker Usage

### Build Docker Image
```bash
docker build -t legal-doc-analyzer .
```

### Run Container
```bash
docker run -p 5000:5000 legal-doc-analyzer
```

### API Testing
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"contract_text": "This agreement shall be governed by California law."}'
```

## 📧 Notifications

The pipeline includes automated email notifications:
- ✅ **Success**: Sent when Docker image is successfully built and pushed
- ❌ **Failure**: Sent when deployment fails
- 📊 **Details**: Includes build information, commit details, and Docker image links

## 🔧 Troubleshooting

### Common Issues

1. **Jenkins Job Not Triggering:**
   - Verify GitHub webhook is configured
   - Check Jenkins credentials and URL in GitHub secrets

2. **Docker Push Fails:**
   - Verify DockerHub credentials in Jenkins
   - Check Docker daemon is running

3. **Email Notifications Not Working:**
   - Verify SMTP settings in Jenkins
   - Check admin email credential is configured

4. **Tests Failing:**
   - Ensure all dependencies are installed
   - Check Python version compatibility

### Debug Commands
```bash
# Check Docker build locally
docker build -t test-image .

# Test application locally
python app/app.py

# Verify requirements
pip check
```

## 📋 Assignment Requirements Compliance

This project fulfills all assignment requirements:

- ✅ **CI/CD Pipeline**: GitHub Actions + Jenkins
- ✅ **Model & Dataset**: LegalBERT + CUAD dataset (unique legal domain)
- ✅ **Tools Used**: Jenkins, GitHub, GitHub Actions, Git, Docker, Python, Flask
- ✅ **Admin Approval**: Branch protection with required reviews
- ✅ **Code Quality**: flake8 integration on dev branch
- ✅ **Branching Strategy**: dev → test → main with appropriate workflows
- ✅ **Unit Testing**: Automated testing on test branch
- ✅ **Containerization**: Docker build and push to DockerHub
- ✅ **Notifications**: Email alerts to administrator

## 👥 Team Setup

For a 2-member team:
1. **Admin**: Full repository access, approves all PRs, receives notifications
2. **Developer**: Write access, creates features, submits PRs for review

## 📚 Additional Resources

- [CUAD Dataset Documentation](https://github.com/TheAtticusProject/cuad)
- [LegalBERT Model](https://huggingface.co/nlpaueb/legal-bert-base-uncased)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📄 License

This project is designed for educational purposes as part of an MLOps assignment.
