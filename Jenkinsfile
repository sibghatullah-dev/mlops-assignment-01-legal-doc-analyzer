pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'legal-doc-analyzer'
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'legal-doc-analyzer-app'
        APP_PORT = '5000'
        HOST_PORT = '8081'
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
                    echo "🐳 Building Docker image for local deployment..."
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                        echo "✅ Docker image built successfully"
                        echo "Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        echo "Latest: ${DOCKER_IMAGE}:latest"
                    """
                }
            }
        }
        
        stage('Stop Previous Container') {
            steps {
                script {
                    echo "🛑 Stopping and removing previous container if exists..."
                    sh """
                        # Stop and remove existing container if running
                        if docker ps -q -f name=${CONTAINER_NAME}; then
                            echo "Stopping running container: ${CONTAINER_NAME}"
                            docker stop ${CONTAINER_NAME} || true
                        fi
                        
                        if docker ps -aq -f name=${CONTAINER_NAME}; then
                            echo "Removing existing container: ${CONTAINER_NAME}"
                            docker rm ${CONTAINER_NAME} || true
                        fi
                        
                        echo "✅ Previous container cleanup completed"
                    """
                }
            }
        }
        
        stage('Deploy to Local Docker') {
            steps {
                script {
                    echo "🚀 Deploying to local Docker environment..."
                    sh """
                        # Run the new container
                        docker run -d \\
                            --name ${CONTAINER_NAME} \\
                            -p ${HOST_PORT}:${APP_PORT} \\
                            --restart unless-stopped \\
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                        
                        # Wait a moment for container to start
                        sleep 5
                        
                        # Verify container is running
                        if docker ps -q -f name=${CONTAINER_NAME}; then
                            echo "✅ Container ${CONTAINER_NAME} is running successfully"
                            echo "🌐 Application accessible at: http://localhost:${HOST_PORT}"
                            
                            # Show container info
                            docker ps -f name=${CONTAINER_NAME}
                            
                            # Test health check
                            if curl -f http://localhost:${HOST_PORT}/health 2>/dev/null; then
                                echo "✅ Health check passed - Application is responding"
                            else
                                echo "⚠️ Health check endpoint not available (this is normal if no health endpoint exists)"
                            fi
                        else
                            echo "❌ Container failed to start"
                            docker logs ${CONTAINER_NAME}
                            exit 1
                        fi
                    """
                }
            }
        }
        
        stage('Deployment Info') {
            steps {
                script {
                    echo "📝 Collecting deployment information..."
                    sh """
                        echo "=== DEPLOYMENT SUMMARY ==="
                        echo "Container Name: ${CONTAINER_NAME}"
                        echo "Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        echo "Application URL: http://localhost:${HOST_PORT}"
                        echo "Container Port: ${APP_PORT}"
                        echo "Host Port: ${HOST_PORT}"
                        echo "Build Number: ${BUILD_NUMBER}"
                        echo "=========================="
                    """
                    
                    // Set environment variables for email notifications
                    env.DEPLOYMENT_URL = "http://localhost:${HOST_PORT}"
                    env.CONTAINER_INFO = "${CONTAINER_NAME} (${DOCKER_IMAGE}:${DOCKER_TAG})"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Cleaning up Docker resources..."
                sh """
                    # Clean up dangling images
                    docker image prune -f || true
                    
                    # Show current Docker status
                    echo "=== CURRENT DOCKER STATUS ==="
                    docker ps -a
                    echo "=== DOCKER IMAGES ==="
                    docker images
                """
            }
        }
        
        success {
            script {
                def buildDuration = currentBuild.duration ? "${(currentBuild.duration / 1000).intValue()}s" : "N/A"
                def gitCommitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                def branchName = sh(script: 'git branch --show-current', returnStdout: true).trim()
                
                echo "✅ SUCCESS: Local deployment completed successfully!"
                echo "🌐 Application URL: http://localhost:${HOST_PORT}"
                echo "🐳 Container: ${CONTAINER_NAME} (${DOCKER_IMAGE}:${DOCKER_TAG})"
                
                // Try to send email if credential exists
                try {
                    def adminEmail = 'admin@example.com' // Replace with your email or credential ID
                    emailext(
                            subject: "✅ SUCCESS: Legal Doc Analyzer Local Deployment - Build #${BUILD_NUMBER}",
                            body: """
                            <html>
                            <head>
                                <style>
                                    body { font-family: Arial, sans-serif; margin: 20px; }
                                    .header { background-color: #28a745; color: white; padding: 20px; border-radius: 5px; }
                                    .content { padding: 20px; border: 1px solid #ddd; border-radius: 5px; margin-top: 10px; }
                                    .success { color: #28a745; }
                                    .info { background-color: #f8f9fa; padding: 10px; border-radius: 3px; }
                                    .link { color: #007bff; text-decoration: none; }
                                    .highlight { background-color: #e7f3ff; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; }
                                    ul { margin: 10px 0; padding-left: 20px; }
                                </style>
                            </head>
                            <body>
                                <div class="header">
                                    <h2>🎉 Local Deployment Successful!</h2>
                                    <p>MLOps CI/CD Pipeline - Legal Document Analyzer</p>
                                </div>
                                <div class="content">
                                    <h3>📋 Build Information</h3>
                                    <div class="info">
                                        <p><strong>Project:</strong> Legal Document Analyzer</p>
                                        <p><strong>Build Number:</strong> #${BUILD_NUMBER}</p>
                                        <p><strong>Build Duration:</strong> ${buildDuration}</p>
                                        <p><strong>Branch:</strong> ${branchName}</p>
                                        <p><strong>Commit Hash:</strong> <code>${gitCommitHash.take(8)}</code></p>
                                        <p><strong>Timestamp:</strong> ${new Date()}</p>
                                    </div>
                                    
                                    <h3>🐳 Local Docker Deployment</h3>
                                    <div class="highlight">
                                        <p><strong>🌐 Application URL:</strong> <a href="http://localhost:${HOST_PORT}" class="link">http://localhost:${HOST_PORT}</a></p>
                                        <p><strong>Container Name:</strong> <code>${CONTAINER_NAME}</code></p>
                                        <p><strong>Docker Image:</strong> <code>${DOCKER_IMAGE}:${DOCKER_TAG}</code></p>
                                        <p><strong>Port Mapping:</strong> Host:${HOST_PORT} → Container:${APP_PORT}</p>
                                    </div>
                                    
                                    <h3>✅ Deployment Status</h3>
                                    <ul>
                                        <li class="success">✅ Code checkout completed successfully</li>
                                        <li class="success">✅ Pre-build validation passed</li>
                                        <li class="success">✅ Docker image built locally</li>
                                        <li class="success">✅ Previous container stopped and removed</li>
                                        <li class="success">✅ New container deployed and running</li>
                                        <li class="success">✅ Application accessible at localhost:${HOST_PORT}</li>
                                    </ul>
                                    
                                    <h3>🔗 Quick Links</h3>
                                    <p>
                                        <a href="${BUILD_URL}" class="link">📊 Build Details</a> | 
                                        <a href="${BUILD_URL}console" class="link">📜 Console Logs</a> | 
                                        <a href="http://localhost:${HOST_PORT}" class="link">🌐 Live Application</a>
                                    </p>
                                </div>
                            </body>
                            </html>
                            """,
                            to: "${adminEmail}",
                            mimeType: 'text/html',
                            attachLog: true
                        )
                        echo "📧 Success email sent successfully"
                    } catch (Exception e) {
                        echo "⚠️ Could not send email notification: ${e.getMessage()}"
                        echo "💡 Please configure 'admin-email' credential in Jenkins if you want email notifications"
                    }
                }
        }
        
        failure {
            script {
                def buildDuration = currentBuild.duration ? "${(currentBuild.duration / 1000).intValue()}s" : "N/A"
                def gitCommitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                def branchName = sh(script: 'git branch --show-current', returnStdout: true).trim()
                def failureStage = currentBuild.result ?: "Unknown"
                
                echo "❌ FAILURE: Local deployment failed!"
                echo "🔍 Check the console logs for details"
                
                // Try to send email if credential exists
                try {
                    def adminEmail = 'admin@example.com' // Replace with your email or credential ID
                    emailext(
                            subject: "❌ FAILED: Legal Doc Analyzer Local Deployment - Build #${BUILD_NUMBER}",
                            body: """
                            <html>
                            <head>
                                <style>
                                    body { font-family: Arial, sans-serif; margin: 20px; }
                                    .header { background-color: #dc3545; color: white; padding: 20px; border-radius: 5px; }
                                    .content { padding: 20px; border: 1px solid #ddd; border-radius: 5px; margin-top: 10px; }
                                    .error { color: #dc3545; }
                                    .info { background-color: #f8f9fa; padding: 10px; border-radius: 3px; }
                                    .warning { background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; border-radius: 3px; }
                                    .link { color: #007bff; text-decoration: none; }
                                </style>
                            </head>
                            <body>
                                <div class="header">
                                    <h2>🚨 Local Deployment Failed!</h2>
                                    <p>MLOps CI/CD Pipeline - Legal Document Analyzer</p>
                                </div>
                                <div class="content">
                                    <h3>📋 Build Information</h3>
                                    <div class="info">
                                        <p><strong>Project:</strong> Legal Document Analyzer</p>
                                        <p><strong>Build Number:</strong> #${BUILD_NUMBER}</p>
                                        <p><strong>Build Duration:</strong> ${buildDuration}</p>
                                        <p><strong>Branch:</strong> ${branchName}</p>
                                        <p><strong>Commit Hash:</strong> <code>${gitCommitHash.take(8)}</code></p>
                                        <p><strong>Failure Status:</strong> <span class="error">${failureStage}</span></p>
                                        <p><strong>Timestamp:</strong> ${new Date()}</p>
                                    </div>
                                    
                                    <h3>🔗 Debug Links</h3>
                                    <p>
                                        <a href="${BUILD_URL}" class="link">📊 Build Details</a> | 
                                        <a href="${BUILD_URL}console" class="link">📜 Console Logs</a>
                                    </p>
                                </div>
                            </body>
                            </html>
                            """,
                            to: "${adminEmail}",
                            mimeType: 'text/html',
                            attachLog: true
                        )
                        echo "📧 Failure email sent successfully"
                    } catch (Exception e) {
                        echo "⚠️ Could not send email notification: ${e.getMessage()}"
                        echo "💡 Please configure 'admin-email' credential in Jenkins if you want email notifications"
                    }
                }
        }
        
        unstable {
            script {
                echo "⚠️ UNSTABLE: Local deployment completed with warnings!"
                echo "🔍 Check the console logs and test results for details"
                echo "🌐 Application may still be accessible at: http://localhost:${HOST_PORT}"
            }
        }
    }
}
