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
                args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
              - name: containerd
                image: gcr.io/kaniko-project/executor:latest
                securityContext:
                  privileged: true
                volumeMounts:
                - name: containerd-socket
                  mountPath: /var/run/containerd/containerd.sock
              volumes:
              - name: containerd-socket
                hostPath:
                  path: /run/containerd/containerd.sock
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
                git branch: 'main', url: 'https://github.com/Leejeuk213/gitops_cicd.git'
            }
        }
        stage('Build Image with ctr') {
            steps {
                container('containerd') {
                    sh 'ctr image build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                }
            }
        }
        stage('Push Image with ctr') {
            steps {
                container('containerd') {
                    withDockerRegistry([credentialsId: 'docker', url: 'https://index.docker.io/v1/']) {
                        sh 'ctr images push ${DOCKER_IMAGE}:${DOCKER_TAG}'
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
