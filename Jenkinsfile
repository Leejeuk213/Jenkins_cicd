pipeline {
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: jnlp
                image: jenkins/inbound-agent:latest
                args:
                - "-secret"
                - "\\$(JENKINS_SECRET)"  # $를 이스케이프 처리
                - "-name"
                - "\\$(JENKINS_NAME)"   # $를 이스케이프 처리
              - name: docker
                image: docker:20.10
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              volumes:
              - name: docker-socket
                hostPath:
                  path: /var/run/docker.sock
                  type: Socket
            """
        }
    }
    environment {
        DOCKER_IMAGE = 'dlwpdnr213/gitops-test'
        DOCKER_TAG = 'latest'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'jenkins', branch: 'main', url: 'https://github.com/Leejeuk213/gitops_cicd.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                container('docker') {
                    withDockerRegistry([credentialsId: 'docker', url: 'https://index.docker.io/v1/']) {
                        sh 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
