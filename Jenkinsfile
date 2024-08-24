pipeline {
    agent {
        docker {
            image 'dashrathpawara/vege-receipe:latest'
             args '--user appuser -v /var/run/docker.sock:/var/run/docker.sock' // mount Docker socket to access the host's Docker daemon
        }
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = 'dashrathpawara/vege-receipe'
    }
    stages {
        stage('Checkout') {
            steps {
                sh 'echoo passed'
                git 'https://github.com/dashrathpawara/django-app.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    def version = getNextVersion()
                    sh "docker build -t ${env.IMAGE_NAME}:${version} ."
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    def version = getNextVersion()
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    sh "docker push ${env.IMAGE_NAME}:${version}"
                }
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
