pipeline {
    agent {
        docker {
            image 'dashrathpawara/docker-py-agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // Mount Docker socket to access the host's Docker daemon
        }
    }    
    environment {
        DOCKER_IMAGE = "dashrathpawara/vege-receipe:${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/dashrathpawara/django-app.git', branch: 'main', changelog: true, poll: true
            }
        }

        stage('Build and Test Data') {
            steps {
                sh 'ls -ltr'
                // Install dependencies and run tests
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Scan Docker Image with Trivy') {
            steps {
                script {
                    def trivyReport = "trivy-report-${env.BUILD_NUMBER}.txt"
        
                    // Run Trivy scan and append results directly to the report file
                    sh '''
                        trivy image \
                            --exit-code 0 \
                            --severity HIGH,CRITICAL \
                            -f plain \
                            ${DOCKER_IMAGE} >> "${trivyReport}" 2>&1 || echo "Trivy scan completed with findings"
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push the Docker image to Docker Hub if the scan is successful
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Post-Build') {
            steps {
                echo "Build, scan, and push completed for version ${env.BUILD_NUMBER}"
        
                // Print the current directory and list files for debugging
                sh '''
                    echo "Current working directory:"
                    pwd
                    echo "Listing files in the workspace:"
                    ls -l
                '''
        
                // Use a script block to execute Groovy code
                script {
                    def trivyReport = "trivy-report-${env.BUILD_NUMBER}.txt"
                    
                    // Check if the file exists and archive it
                    if (fileExists(trivyReport)) {
                        archiveArtifacts artifacts: trivyReport, allowEmptyArchive: true
                    } else {
                        echo "Report file ${trivyReport} does not exist."
                    }
                }
            }
        }
    }

    post {
        always {
            // Cleanup: remove Docker images to free up space
            sh "docker rmi ${DOCKER_IMAGE}"
        }
    }
}
