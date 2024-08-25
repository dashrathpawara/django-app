pipeline {
    agent {
        docker {
            image 'dashrathpawara/vege-receipe:1'
             args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // mount Docker socket to access the host's Docker daemon
        }
    }    
    stages {
        stage('Checkout') {
    steps {
        git url: 'https://github.com/dashrathpawara/django-app.git', branch: 'main', changelog: true, poll: true
    }
}

        stage('Build and Test') {
            steps {
                sh 'ls -ltr'
                // Install dependencies and run tests
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }
        stage('Build and Push Docker Image') {
            environment {
                DOCKER_IMAGE = "dashrathpawara/vege-receipe:${BUILD_NUMBER}"
                REGISTRY_CREDENTIALS = credentials('dockerhub-credentials')
            }
            steps {
                script {
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                    def dockerImage = docker.image("${DOCKER_IMAGE}")
                    docker.withRegistry('https://index.docker.io/v1/', "${REGISTRY_CREDENTIALS}") 
                    {
                        dockerImage.push()
                    }
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

