pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DOCKER_ID = 'r4misw'
        DOCKER_IMAGE = 'datascientestapi'
        DOCKER_TAG = "v.${BUILD_ID}.0"
        CONTAINER_NAME = 'jenkins'
    }

    stages {
        stage('Building') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD":/workspace \
                      -w /workspace \
                      -e PYTHONDONTWRITEBYTECODE=1 \
                      python:3.11-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt"
                '''
            }
        }

        stage('Testing') {
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

        stage('Deploying') {
            steps {
                script {
                    sh '''
                        docker rm -f ${CONTAINER_NAME} || true
                        docker build -t ${DOCKER_ID}/${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker run -d -p 8000:8000 --name ${CONTAINER_NAME} ${DOCKER_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }

        stage('User Acceptance') {
            steps {
                input {
                    message 'Proceed to push image to Docker Hub?'
                    ok 'Yes'
                }
            }
        }

        stage('Pushing and Merging') {
            parallel {
                stage('Pushing Image') {
                    environment {
                        DOCKERHUB_CREDENTIALS = credentials('docker_jenkins')
                    }
                    steps {
                        sh '''
                            echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                            docker push ${DOCKER_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        '''
                    }
                }

                stage('Merging') {
                    steps {
                        echo 'Merging done'
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}