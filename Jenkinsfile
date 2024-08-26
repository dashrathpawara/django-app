pipeline {
    agent {
        docker {
            image 'dashrathpawara/vege-receipe:0.0.0'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // Mount Docker socket to access the host's Docker daemon
        }
    }    
    environment {
        DOCKER_IMAGE = "dashrathpawara/vege-receipe:${getNextVersion()}"
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

        stage('Push Docker Image') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Post-Build') {
            steps {
                echo "Build and push completed for version ${DOCKER_IMAGE.split(':')[1]}"
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

// Function to calculate the next version based on the latest Git tag
def getNextVersion() {
    def version = sh(script: "git describe --tags --abbrev=0", returnStdout: true).trim()
    def (major, minor, patch) = version.tokenize('.')
    patch = patch.toInteger() + 1
    return "${major}.${minor}.${patch}"
}
