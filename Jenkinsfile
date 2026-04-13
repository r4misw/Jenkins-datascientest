pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DOCKER_IMAGE = 'datascientestapi'
        DOCKER_TAG = "v.${BUILD_ID}.0"
        CONTAINER_NAME = 'jenkins'
        GITHUB_REPO = 'r4misw/Jenkins-datascientest'
        STATUS_CONTEXT = 'jenkins/pr-ci'
    }

    stages {
        stage('Set Pending Status') {
            steps {
                withCredentials([string(credentialsId: 'github_status_token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        cat > status.json <<EOF
{"state":"pending","context":"${STATUS_CONTEXT}","description":"Jenkins pipeline is running","target_url":"${BUILD_URL}"}
EOF
                        curl -s -X POST \
                          -H "Accept: application/vnd.github+json" \
                          -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                          https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                          -d @status.json >/dev/null
                        rm -f status.json
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -m unittest -v'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d -p 8000:8000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }

        stage('Approve Release') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Publish the official Docker image?', ok: 'Publish'
            }
        }

        stage('Publish Image') {
            when {
                branch 'main'
            }
            environment {
                DOCKERHUB_CREDENTIALS = credentials('docker_jenkins')
            }
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
    }

    post {
        success {
            withCredentials([string(credentialsId: 'github_status_token', variable: 'GITHUB_TOKEN')]) {
                sh '''
                    cat > status.json <<EOF
{"state":"success","context":"${STATUS_CONTEXT}","description":"Jenkins pipeline succeeded","target_url":"${BUILD_URL}"}
EOF
                    curl -s -X POST \
                      -H "Accept: application/vnd.github+json" \
                      -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                      https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                      -d @status.json >/dev/null
                    rm -f status.json
                '''
            }
        }
        failure {
            withCredentials([string(credentialsId: 'github_status_token', variable: 'GITHUB_TOKEN')]) {
                sh '''
                    cat > status.json <<EOF
{"state":"failure","context":"${STATUS_CONTEXT}","description":"Jenkins pipeline failed","target_url":"${BUILD_URL}"}
EOF
                    curl -s -X POST \
                      -H "Accept: application/vnd.github+json" \
                      -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                      https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                      -d @status.json >/dev/null
                    rm -f status.json
                '''
            }
        }
        aborted {
            withCredentials([string(credentialsId: 'github_status_token', variable: 'GITHUB_TOKEN')]) {
                sh '''
                    cat > status.json <<EOF
{"state":"error","context":"${STATUS_CONTEXT}","description":"Jenkins pipeline was aborted","target_url":"${BUILD_URL}"}
EOF
                    curl -s -X POST \
                      -H "Accept: application/vnd.github+json" \
                      -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                      https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                      -d @status.json >/dev/null
                    rm -f status.json
                '''
            }
        }
        always {
            sh 'docker logout || true'
        }
    }
}