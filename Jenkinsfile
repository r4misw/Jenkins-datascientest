pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        IMAGE_NAME = 'flask-api-demo'
        CONTAINER_NAME = 'flask-api-demo'
    }

    stages {
        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD":/workspace \
                      -w /workspace \
                      -e PYTHONDONTWRITEBYTECODE=1 \
                      python:3.11-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt && python -m unittest -v"
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        success {
            echo 'Application deployed on port 5000.'
        }
    }
}