# 🚀 Complete CI/CD Pipeline Setup Guide

This guide will walk you through setting up the entire CI/CD pipeline for your MLOps assignment step by step.

## 📚 Understanding the Tools

### What is Jenkins?
Jenkins is an open-source automation server that helps you build, test, and deploy your applications. In our assignment, Jenkins will:
- Build Docker containers from your code
- Push containers to Docker Hub
- Send email notifications to admins

### What is Docker Hub?
Docker Hub is a cloud-based registry where you can store and share Docker images. Think of it as "GitHub for Docker containers."

### What are GitHub Secrets?
GitHub Secrets are encrypted environment variables that store sensitive information (passwords, tokens) securely in your repository.

### What are Branch Protection Rules?
These are GitHub settings that enforce workflows - like requiring code reviews before merging branches.

---

## 🔧 STEP 1: Setting up Docker Hub Account

### 1.1 Create Docker Hub Account
1. Go to [https://hub.docker.com](https://hub.docker.com)
2. Click "Sign Up" and create a free account
3. Choose a username (e.g., `your-username`) - remember this!
4. Verify your email address

### 1.2 Create a Repository on Docker Hub
1. After logging in, click "Create Repository"
2. Repository name: `legal-doc-analyzer`
3. Description: "Legal Document Analyzer for MLOps Assignment"
4. Set visibility to "Public" (free tier)
5. Click "Create"

### 1.3 Generate Access Token (Important for Security)
1. Click on your profile picture → "Account Settings"
2. Go to "Security" tab
3. Click "New Access Token"
4. Token description: "Jenkins CI/CD Pipeline"
5. Access permissions: "Read, Write, Delete"
6. Click "Generate"
7. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!
8. Save it somewhere safe (e.g., notepad)

**Example:**
```
Docker Hub Username: john-doe
Docker Hub Token: dckr_pat_1234567890abcdef (this is fake - yours will be different)
```

---

## 🔧 STEP 2: Setting up Jenkins

### 2.1 Install Jenkins (Choose your method)

#### Option A: Using Docker (Recommended for beginners)
```bash
# Pull Jenkins Docker image
docker pull jenkins/jenkins:lts

# Run Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

#### Option B: Ubuntu/Debian Installation
```bash
# Update system
sudo apt update

# Install Java (Jenkins requirement)
sudo apt install openjdk-11-jdk -y

# Add Jenkins repository
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

# Install Jenkins
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### 2.2 Initial Jenkins Setup
1. Open browser and go to `http://localhost:8080`
2. You'll see "Unlock Jenkins" page
3. Get the initial admin password:

**If using Docker:**
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

**If installed directly:**
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

4. Copy the password and paste it in the web interface
5. Click "Install suggested plugins" (wait for installation)
6. Create admin user:
   - Username: `admin`
   - Password: `your-secure-password`
   - Full name: `Admin User`
   - Email: `your-email@example.com`
7. Jenkins URL: Keep default `http://localhost:8080/`
8. Click "Start using Jenkins"

### 2.3 Install Required Jenkins Plugins
1. Go to "Manage Jenkins" → "Manage Plugins"
2. Click "Available" tab
3. Search and install these plugins:
   - **Docker Pipeline** (for Docker operations)
   - **Email Extension** (for email notifications)
   - **GitHub Integration** (for GitHub webhooks)
   - **Pipeline** (should already be installed)
4. Check "Restart Jenkins when installation is complete"

---

## 🔧 STEP 3: Configuring Jenkins Credentials

### 3.1 Add Docker Hub Credentials
1. Go to "Manage Jenkins" → "Manage Credentials"
2. Click "(global)" under "Stores scoped to Jenkins"
3. Click "Add Credentials"
4. Fill out the form:
   - **Kind**: "Username with password"
   - **Scope**: "Global"
   - **Username**: Your Docker Hub username (e.g., `john-doe`)
   - **Password**: Your Docker Hub access token (from Step 1.3)
   - **ID**: `docker-hub-credentials` (EXACTLY this - case sensitive!)
   - **Description**: "Docker Hub credentials for CI/CD"
5. Click "OK"

### 3.2 Add Admin Email Credential
1. Click "Add Credentials" again
2. Fill out the form:
   - **Kind**: "Secret text"
   - **Scope**: "Global"
   - **Secret**: Your admin email address (e.g., `admin@example.com`)
   - **ID**: `admin-email` (EXACTLY this!)
   - **Description**: "Admin email for notifications"
3. Click "OK"

### 3.3 Configure Email Settings (IMPORTANT for notifications)
1. Go to "Manage Jenkins" → "Configure System"
2. Scroll down to "Extended E-mail Notification" section
3. Configure your SMTP settings:

**For Gmail:**
```
SMTP server: smtp.gmail.com
SMTP port: 587
Use SMTP Authentication: ✓
Username: your-gmail@gmail.com
Password: your-app-password (see note below)
Use SSL: ✓
```

**Gmail App Password Setup:**
1. Go to Google Account settings
2. Security → 2-Step Verification (enable if not already)
3. Search for "App passwords"
4. Select app: "Mail", device: "Other (custom name)"
5. Type: "Jenkins CI/CD"
6. Copy the generated 16-character password

4. Test email configuration by clicking "Test configuration"
5. Scroll down to "Default Recipients": Enter admin email
6. Click "Save"

---

## 🔧 STEP 4: Creating Jenkins Job

### 4.1 Create Pipeline Job
1. From Jenkins dashboard, click "New Item"
2. Enter name: `legal-doc-analyzer-deploy`
3. Select "Pipeline"
4. Click "OK"

### 4.2 Configure Pipeline
1. In the job configuration page:
   - **Description**: "Legal Document Analyzer CI/CD Pipeline"
   - **GitHub project**: ✓ (check this)
   - **Project url**: `https://github.com/sibghatullah-dev/mlops-assignment-01`

2. Scroll to "Build Triggers" section:
   - ✓ **GitHub hook trigger for GITScm polling**

3. Scroll to "Pipeline" section:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/sibghatullah-dev/mlops-assignment-01.git`
   - **Branches to build**: `*/master` (or `*/main`)
   - **Script Path**: `Jenkinsfile`

4. Click "Save"

### 4.3 Test Jenkins Job
1. Click "Build Now" to test the pipeline
2. Check "Console Output" for any errors
3. If successful, you should see your Docker image on Docker Hub

---

## 🔧 STEP 5: Setting up GitHub Secrets

### 5.1 Access Repository Secrets
1. Go to your GitHub repository: `https://github.com/sibghatullah-dev/mlops-assignment-01`
2. Click "Settings" tab (top of repository)
3. In left sidebar, click "Secrets and variables" → "Actions"

### 5.2 Add Required Secrets
Click "New repository secret" for each of these:

#### Secret 1: JENKINS_URL
- **Name**: `JENKINS_URL`
- **Secret**: `http://your-jenkins-server:8080` 
  - If Jenkins is on same machine: `http://localhost:8080`
  - If Jenkins is on different server: `http://your-server-ip:8080`
  - If using cloud: `https://your-jenkins-domain.com`

#### Secret 2: JENKINS_USER
- **Name**: `JENKINS_USER`
- **Secret**: `admin` (or whatever username you created)

#### Secret 3: JENKINS_TOKEN
- **Name**: `JENKINS_TOKEN`
- **Secret**: Jenkins API token (see below how to get it)

### 5.3 Generate Jenkins API Token
1. In Jenkins, click your username (top right)
2. Click "Configure"
3. Scroll to "API Token" section
4. Click "Add new Token"
5. Token name: "GitHub Actions"
6. Click "Generate"
7. **COPY THE TOKEN IMMEDIATELY**
8. Use this token as the `JENKINS_TOKEN` secret

---

## 🔧 STEP 6: Setting up Branch Protection Rules

### 6.1 Protect the Master Branch
1. Go to repository "Settings" → "Branches"
2. Click "Add rule" or "Add branch protection rule"
3. Branch name pattern: `master` (or `main`)
4. Configure protection settings:

#### Required Settings:
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals**: 1
  - ✅ **Dismiss stale PR approvals when new commits are pushed**
  - ✅ **Require review from code owners**

- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**
  - Search for and select status checks:
    - `unit-tests` (from test.yml workflow)
    - `code-quality` (from lint.yml workflow)

- ✅ **Require conversation resolution before merging**
- ✅ **Include administrators** (enforces rules for admins too)

5. Click "Create"

### 6.2 Protect the Test Branch
1. Click "Add rule" again
2. Branch name pattern: `test`
3. Configure similar settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals**: 1
   - ✅ **Require status checks**: Select `unit-tests`
4. Click "Create"

### 6.3 Protect the Dev Branch
1. Click "Add rule" again
2. Branch name pattern: `dev`
3. Configure settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals**: 1
   - ✅ **Require status checks**: Select `code-quality`
4. Click "Create"

---

## 🔧 STEP 7: Setting up Webhooks (Optional but Recommended)

### 7.1 Configure GitHub Webhook for Jenkins
1. Go to repository "Settings" → "Webhooks"
2. Click "Add webhook"
3. **Payload URL**: `http://your-jenkins-server:8080/github-webhook/`
4. **Content type**: `application/json`
5. **Which events**: Select "Just the push event"
6. ✅ **Active**
7. Click "Add webhook"

---

## 🧪 STEP 8: Testing the Complete Pipeline

### 8.1 Test the Workflow
Create a simple test to verify everything works:

1. **Create a feature branch from dev:**
```bash
git checkout dev
git checkout -b feature/test-pipeline
```

2. **Make a small change (e.g., update README):**
```bash
echo "# Test change for CI/CD pipeline" >> README.md
git add README.md
git commit -m "Test: Add pipeline test documentation"
git push origin feature/test-pipeline
```

3. **Create Pull Request to dev branch:**
   - Go to GitHub → "Pull requests" → "New pull request"
   - Base: `dev` ← Compare: `feature/test-pipeline`
   - Title: "Test: CI/CD Pipeline Validation"
   - Create pull request

4. **Observe automated checks:**
   - GitHub Actions should run flake8 code quality check
   - You should see status checks in the PR

5. **Merge to dev** (after approval)

6. **Create PR from dev to test:**
   - Base: `test` ← Compare: `dev`
   - This should trigger unit tests

7. **Create PR from test to master:**
   - Base: `master` ← Compare: `test`
   - This should trigger Jenkins deployment

### 8.2 Verify Each Step
- ✅ Code quality check runs on dev
- ✅ Unit tests run on test  
- ✅ Jenkins builds and pushes Docker image
- ✅ Admin receives email notification
- ✅ Docker image appears on Docker Hub

---

## 🔧 STEP 9: Setting up Team Collaboration

### 9.1 Add Team Member as Collaborator
1. Go to repository "Settings" → "Collaborators"
2. Click "Add people"
3. Enter your teammate's GitHub username
4. Select permission level: "Write"
5. Click "Add [username] to this repository"

### 9.2 Assign Admin Role
1. One team member should be designated as admin
2. Admin should have "Admin" permission on the repository
3. Admin will be responsible for:
   - Reviewing and approving pull requests
   - Merging code between branches
   - Monitoring Jenkins jobs
   - Responding to email notifications

---

## 🚨 Troubleshooting Common Issues

### Issue 1: Jenkins Can't Access Docker
**Error**: "docker: command not found"

**Solution**: Install Docker on Jenkins server:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Issue 2: GitHub Actions Can't Trigger Jenkins
**Error**: Connection refused

**Solution**: 
1. Check Jenkins is accessible from internet
2. If using localhost, consider using ngrok for testing:
```bash
# Install ngrok
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
./ngrok http 8080
# Use the ngrok URL as JENKINS_URL secret
```

### Issue 3: Email Notifications Not Working
**Solution**:
1. Check SMTP settings in Jenkins
2. Verify app password for Gmail
3. Test email configuration in Jenkins

### Issue 4: Docker Hub Push Fails
**Error**: "authentication required"

**Solution**:
1. Verify Docker Hub credentials in Jenkins
2. Check Docker Hub access token is valid
3. Ensure repository exists on Docker Hub

---

## 📋 Final Checklist

Before submitting your assignment, verify:

- [ ] Docker Hub account created with repository
- [ ] Jenkins installed and configured
- [ ] Jenkins credentials added (docker-hub-credentials, admin-email)
- [ ] Email notifications configured
- [ ] GitHub secrets added (JENKINS_URL, JENKINS_USER, JENKINS_TOKEN)
- [ ] Branch protection rules configured for all branches
- [ ] Team member added as collaborator
- [ ] Admin role assigned
- [ ] Complete workflow tested (dev → test → master)
- [ ] Docker image successfully pushed to Docker Hub
- [ ] Admin receives email notifications

---

## 📚 Understanding the Assignment Requirements

Your assignment asked for:
1. ✅ **Jenkins + GitHub + Docker integration**
2. ✅ **Admin approval system** (Branch protection rules)
3. ✅ **Code quality checks with flake8** (GitHub Actions on dev)
4. ✅ **Unit testing workflow** (GitHub Actions on test)
5. ✅ **Containerization and Docker Hub push** (Jenkins on master)
6. ✅ **Email notifications** (Jenkins post-build actions)

This setup implements all requirements with industry-standard practices!

---

## 🎯 Success Criteria

Your pipeline is working correctly when:
1. Code pushed to dev triggers flake8 quality checks
2. PR from dev to test requires admin approval and triggers unit tests
3. PR from test to master requires admin approval and triggers Jenkins
4. Jenkins builds Docker image and pushes to Docker Hub
5. Admin receives detailed email notification
6. Docker image is publicly available on Docker Hub

**Congratulations! You've built a production-ready CI/CD pipeline! 🚀**