# 🚀 Quick Reference Card - CI/CD Pipeline Setup

## 📝 Essential Information You'll Need

### Docker Hub Setup
```
Account: [Create at hub.docker.com]
Repository: legal-doc-analyzer
Access Token: [Generate in Security settings]
```

### Jenkins Credentials (Exact IDs - Case Sensitive!)
```
ID: docker-hub-credentials
Type: Username with password
Username: [Your Docker Hub username]
Password: [Your Docker Hub access token]

ID: admin-email  
Type: Secret text
Secret: [Your admin email]
```

### GitHub Secrets (Exact Names!)
```
JENKINS_URL: http://your-jenkins-server:8080
JENKINS_USER: admin
JENKINS_TOKEN: [Generate in Jenkins user settings]
```

## 🔄 Workflow Summary

```
Feature Branch → dev (flake8) → test (pytest) → master (Jenkins → Docker Hub + Email)
```

## ⚡ Quick Commands

### Start Jenkins (Docker)
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Get Jenkins Initial Password
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Test Docker Build Locally
```bash
docker build -t legal-doc-analyzer .
docker run -p 5000:5000 legal-doc-analyzer
```

### Test Code Quality
```bash
flake8 --config .flake8 app/ model/ tests/
```

### Run Unit Tests
```bash
pytest tests/ -v
```

## 🎯 Required Jenkins Plugins
- Docker Pipeline
- Email Extension  
- GitHub Integration
- Pipeline

## 📧 Gmail SMTP Settings
```
Server: smtp.gmail.com
Port: 587
Authentication: ✓
SSL: ✓
Username: your-gmail@gmail.com
Password: [16-character app password]
```

## 🛡️ Branch Protection Rules

### Master Branch
- Require PR approval
- Require status checks: unit-tests, code-quality
- Include administrators

### Test Branch  
- Require PR approval
- Require status checks: unit-tests

### Dev Branch
- Require PR approval  
- Require status checks: code-quality

## 🧪 Testing the Pipeline

1. Create feature branch from dev
2. Make change, push to GitHub
3. Create PR: feature → dev (triggers flake8)
4. Admin approves, merge to dev
5. Create PR: dev → test (triggers pytest)  
6. Admin approves, merge to test
7. Create PR: test → master (triggers Jenkins)
8. Admin approves, merge to master
9. Jenkins builds Docker image
10. Admin receives email notification

## 🚨 Common Issues & Solutions

### Jenkins can't find Docker
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### GitHub can't reach Jenkins
- Use ngrok for local testing
- Check firewall settings
- Verify Jenkins URL in secrets

### Email not working
- Enable 2FA on Gmail
- Generate app password
- Test configuration in Jenkins

## 📞 Support Resources

- **Jenkins Documentation**: https://www.jenkins.io/doc/
- **Docker Hub Help**: https://docs.docker.com/docker-hub/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Flask Documentation**: https://flask.palletsprojects.com/

Remember: This is an MLOps assignment demonstrating industry-standard CI/CD practices!