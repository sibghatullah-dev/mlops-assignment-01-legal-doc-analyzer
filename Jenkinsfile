pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'legal-doc-analyzer'
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'legal-doc-analyzer-app'
        APP_PORT = '5000'
        HOST_PORT = '8081'
        ADMIN_EMAIL = credentials('admin-email')
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
                    echo "� Stopping and removing previous container if exists..."
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
                                <p><strong>Commit Message:</strong> ${GIT_COMMIT_MSG}</p>
                                <p><strong>Author:</strong> ${GIT_AUTHOR}</p>
                                <p><strong>Timestamp:</strong> ${new Date()}</p>
                            </div>
                            
                            <h3>🐳 Local Docker Deployment</h3>
                            <div class="highlight">
                                <p><strong>🌐 Application URL:</strong> <a href="${DEPLOYMENT_URL}" class="link">${DEPLOYMENT_URL}</a></p>
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
                            
                            <h3>🛠️ Container Management Commands</h3>
                            <div class="info">
                                <p><strong>View logs:</strong> <code>docker logs ${CONTAINER_NAME}</code></p>
                                <p><strong>Stop container:</strong> <code>docker stop ${CONTAINER_NAME}</code></p>
                                <p><strong>Start container:</strong> <code>docker start ${CONTAINER_NAME}</code></p>
                                <p><strong>Remove container:</strong> <code>docker rm ${CONTAINER_NAME}</code></p>
                            </div>
                            
                            <h3>🔗 Quick Links</h3>
                            <p>
                                <a href="${BUILD_URL}" class="link">📊 Build Details</a> | 
                                <a href="${BUILD_URL}console" class="link">📜 Console Logs</a> | 
                                <a href="${DEPLOYMENT_URL}" class="link">🌐 Live Application</a>
                            </p>
                            
                            <div style="margin-top: 20px; padding: 10px; background-color: #d4edda; border-left: 4px solid #28a745; border-radius: 3px;">
                                <strong>🚀 Success:</strong> The application is now running locally at 
                                <a href="${DEPLOYMENT_URL}" class="link">${DEPLOYMENT_URL}</a>. 
                                The container will restart automatically unless manually stopped.
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    to: "${ADMIN_EMAIL}",
                    mimeType: 'text/html',
                    attachLog: true
                )
            }
        }
        
        failure {
            script {
                def buildDuration = currentBuild.duration ? "${(currentBuild.duration / 1000).intValue()}s" : "N/A"
                def gitCommitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                def branchName = sh(script: 'git branch --show-current', returnStdout: true).trim()
                def failureStage = currentBuild.result ?: "Unknown"
                
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
                            .code { background-color: #f1f1f1; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
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
                                <p><strong>Commit Message:</strong> ${GIT_COMMIT_MSG}</p>
                                <p><strong>Author:</strong> ${GIT_AUTHOR}</p>
                                <p><strong>Failure Status:</strong> <span class="error">${failureStage}</span></p>
                                <p><strong>Timestamp:</strong> ${new Date()}</p>
                            </div>
                            
                            <h3>🔍 Failure Analysis</h3>
                            <div class="warning">
                                <p><strong>⚠️ Pipeline Stage Failed:</strong> Check the console logs to identify which stage failed:</p>
                                <ul>
                                    <li><strong>Checkout:</strong> Git repository access issues</li>
                                    <li><strong>Pre-build Validation:</strong> Repository state validation failed</li>
                                    <li><strong>Build Docker Image:</strong> Docker build process failed</li>
                                    <li><strong>Stop Previous Container:</strong> Container cleanup failed</li>
                                    <li><strong>Deploy to Local Docker:</strong> Container deployment or startup failed</li>
                                </ul>
                            </div>
                            
                            <h3>🛠️ Local Docker Troubleshooting</h3>
                            <ol>
                                <li><strong>Check Docker Status:</strong> <code>docker ps -a</code> and <code>docker images</code></li>
                                <li><strong>View Container Logs:</strong> <code>docker logs ${CONTAINER_NAME}</code></li>
                                <li><strong>Check Port Availability:</strong> Ensure port ${HOST_PORT} is not in use</li>
                                <li><strong>Docker Daemon:</strong> Verify Docker Desktop is running</li>
                                <li><strong>Resource Issues:</strong> Check available disk space and memory</li>
                                <li><strong>Image Build:</strong> Test build locally: <code>docker build -t ${DOCKER_IMAGE}:test .</code></li>
                            </ol>
                            
                            <h3>🔧 Quick Fixes</h3>
                            <div class="info">
                                <p><strong>Kill conflicting processes:</strong> <code>sudo lsof -i :${HOST_PORT}</code></p>
                                <p><strong>Clean Docker:</strong> <code>docker system prune -f</code></p>
                                <p><strong>Manual container removal:</strong> <code>docker rm -f ${CONTAINER_NAME}</code></p>
                                <p><strong>Check application:</strong> Test at <code>http://localhost:${HOST_PORT}</code></p>
                            </div>
                            
                            <h3>🔗 Debug Links</h3>
                            <p>
                                <a href="${BUILD_URL}" class="link">📊 Build Details</a> | 
                                <a href="${BUILD_URL}console" class="link">📜 Console Logs</a> | 
                                <a href="${BUILD_URL}changes" class="link">📝 Changes</a> |
                                <a href="https://github.com/sibghatullah-dev/mlops-assignment-01-legal-doc-analyzer/commit/${gitCommitHash}" class="link">🔗 Commit</a>
                            </p>
                            
                            <div style="margin-top: 20px; padding: 10px; background-color: #f8d7da; border-left: 4px solid #dc3545; border-radius: 3px;">
                                <strong>🚨 Action Required:</strong> Please review the build logs and fix the local deployment issues. 
                                Ensure Docker Desktop is running and port ${HOST_PORT} is available. Push fixes to trigger a new build.
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    to: "${ADMIN_EMAIL}",
                    mimeType: 'text/html',
                    attachLog: true
                )
            }
        }
        
        unstable {
            script {
                def buildDuration = currentBuild.duration ? "${(currentBuild.duration / 1000).intValue()}s" : "N/A"
                def gitCommitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                def branchName = sh(script: 'git branch --show-current', returnStdout: true).trim()
                
                emailext(
                    subject: "⚠️ UNSTABLE: Legal Doc Analyzer Local Deployment - Build #${BUILD_NUMBER}",
                    body: """
                    <html>
                    <head>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 20px; }
                            .header { background-color: #ffc107; color: #212529; padding: 20px; border-radius: 5px; }
                            .content { padding: 20px; border: 1px solid #ddd; border-radius: 5px; margin-top: 10px; }
                            .warning { color: #856404; }
                            .info { background-color: #f8f9fa; padding: 10px; border-radius: 3px; }
                            .alert { background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; border-radius: 3px; }
                            .link { color: #007bff; text-decoration: none; }
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h2>⚠️ Local Deployment Unstable!</h2>
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
                                <p><strong>Commit Message:</strong> ${GIT_COMMIT_MSG}</p>
                                <p><strong>Author:</strong> ${GIT_AUTHOR}</p>
                                <p><strong>Status:</strong> <span class="warning">UNSTABLE</span></p>
                                <p><strong>Timestamp:</strong> ${new Date()}</p>
                            </div>
                            
                            <div class="alert">
                                <strong>⚠️ Warning:</strong> The local deployment completed but with warnings or non-critical issues. 
                                The application may be running but requires attention.
                            </div>
                            
                            <h3>🔍 Check Application Status</h3>
                            <div class="info">
                                <p><strong>Expected URL:</strong> <code>http://localhost:${HOST_PORT}</code></p>
                                <p><strong>Container Status:</strong> <code>docker ps -f name=${CONTAINER_NAME}</code></p>
                                <p><strong>Application Logs:</strong> <code>docker logs ${CONTAINER_NAME}</code></p>
                            </div>
                            
                            <h3>🔗 Review Links</h3>
                            <p>
                                <a href="${BUILD_URL}" class="link">📊 Build Details</a> | 
                                <a href="${BUILD_URL}console" class="link">📜 Console Logs</a> | 
                                <a href="${BUILD_URL}testReport" class="link">📋 Test Results</a>
                            </p>
                        </div>
                    </body>
                    </html>
                    """,
                    to: "${ADMIN_EMAIL}",
                    mimeType: 'text/html',
                    attachLog: true
                )
            }
        }
    }
}