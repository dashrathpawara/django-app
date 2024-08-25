pipeline {
    agent {
        docker {
            image 'dashrathpawara/vege-receipe:latest'
             args '--user appuser -v /var/run/docker.sock:/var/run/docker.sock' // mount Docker socket to access the host's Docker daemon
        }
    }
    
    stages {
        stage('Checkout') {
            steps {
                sh 'echo passed'
                git 'https://github.com/dashrathpawara/django-app.git'
            }
        }
        stage('Build and Push Docker Image') {
            environment {
                IMAGE_NAME = "dashrathpawara/vege-receipe:${getNextVersion()}"
                DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
                
            }
            steps {
                script {
                    def version = getNextVersion()
                    sh "docker build -t ${env.IMAGE_NAME}:${version} ."
                }
            }
            steps {
                script {
                    def version = getNextVersion()
                    docker.withRegistry('https://index.docker.io/v1/', "dockerhub-credentials") {
                    dockerImage.push()
                }
            }
        stage('Post-Build') {
            steps {
                echo "Build and push completed for version ${getNextVersion()}"
            }
        }
    }
}

def getNextVersion() {
    def version = sh(script: "git describe --tags --abbrev=0", returnStdout: true).trim()
    def (major, minor, patch) = version.tokenize('.')
    patch = patch.toInteger() + 1
    return "${major}.${minor}.${patch}"
}
