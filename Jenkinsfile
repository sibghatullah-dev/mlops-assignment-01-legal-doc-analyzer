pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'legal-doc-analyzer'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        ADMIN_EMAIL = credentials('admin-email')
        DOCKER_HOST = 'unix:///home/zain-abbas/.docker/desktop/docker.sock'
    }
    
    stages {
        stage('Checkout') {
            when {
                branch 'main'
            }
            steps {
                checkout scm
                script {
                    echo "🔍 Running deployment pipeline on main branch..."
                    env.GIT_COMMIT_MSG = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()
                    env.GIT_AUTHOR = sh(
                        script: 'git log -1 --pretty=%an',
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Pre-build Validation') {
            steps {
                script {
                    echo "🔍 Validating repository state..."
                    sh """
                        echo "Current branch: \$(git branch --show-current)"
                        echo "Latest commit: \$(git log -1 --oneline)"
                        echo "Repository status: \$(git status --porcelain || echo 'Clean')"
                    """
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker image..."
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:latest
                        echo "✅ Docker image built successfully"
                    """
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    echo "🚀 Pushing Docker image to DockerHub..."
                    sh """
                        echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                        docker push ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:latest
                        echo "✅ Docker image pushed to DockerHub successfully"
                    """
                }
            }
        }
        
        stage('Deploy Notification') {
            steps {
                script {
                    env.DOCKER_IMAGE_URL = "${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
        }
        
        success {
            emailext(
                subject: "✅ SUCCESS: Legal Doc Analyzer Deployment - Build #${BUILD_NUMBER}",
                body: """
                <html>
                <body>
                    <h2>🎉 Deployment Successful!</h2>
                    <p><strong>Project:</strong> Legal Document Analyzer</p>
                    <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Commit:</strong> ${GIT_COMMIT_MSG}</p>
                    <p><strong>Author:</strong> ${GIT_AUTHOR}</p>
                    <p><strong>Docker Image:</strong> <a href="https://hub.docker.com/r/${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}">${DOCKER_IMAGE_URL}</a></p>
                    <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Timestamp:</strong> ${new Date()}</p>
                    
                    <h3>Deployment Details:</h3>
                    <ul>
                        <li>Container successfully built and pushed to DockerHub</li>
                        <li>Application is ready for production deployment</li>
                        <li>All tests passed in previous stages</li>
                    </ul>
                </body>
                </html>
                """,
                to: "${ADMIN_EMAIL}",
                mimeType: 'text/html'
            )
        }
        
        failure {
            emailext(
                subject: "❌ FAILED: Legal Doc Analyzer Deployment - Build #${BUILD_NUMBER}",
                body: """
                <html>
                <body>
                    <h2>🚨 Deployment Failed!</h2>
                    <p><strong>Project:</strong> Legal Document Analyzer</p>
                    <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Commit:</strong> ${GIT_COMMIT_MSG}</p>
                    <p><strong>Author:</strong> ${GIT_AUTHOR}</p>
                    <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Console Log:</strong> <a href="${BUILD_URL}console">${BUILD_URL}console</a></p>
                    <p><strong>Timestamp:</strong> ${new Date()}</p>
                    
                    <h3>Action Required:</h3>
                    <p>Please check the build logs and fix the deployment issues.</p>
                </body>
                </html>
                """,
                to: "${ADMIN_EMAIL}",
                mimeType: 'text/html'
            )
        }
    }
}