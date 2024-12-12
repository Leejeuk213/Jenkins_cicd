pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'dlwpdnr213/gitops-test'
        GIT_COMMIT_HASH = ''
        TAG = ''
        JENKINS_REPO = 'https://github.com/Leejeuk213/gitops_cicd.git'
        ARGOCD_REPO = 'https://github.com/Leejeuk213/argocd_yaml.git'
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    GIT_COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    TAG = "build-${GIT_COMMIT_HASH}"
                }
            }
        }

        // stage('Git Config Setup') {
        //     steps {
        //         script {
        //             sh 'git config --global user.name "Leejeuk213"'
        //             sh 'git config --global user.email "dlwpdnr213@naver.com"'
        //         }
        //     }
        // }

        stage('Clone Repository') {
            steps {
                git credentialsId: 'jenkins', branch: 'main', url: JENKINS_REPO
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withDockerRegistry([credentialsId: 'docker', url: 'https://index.docker.io/v1/']) {
                        sh "docker push ${DOCKER_IMAGE}:${TAG}"
                    }
                }
            }
        }

        stage('Update Argo CD Configuration') {
            steps {
                script {
                    dir('argocd_yaml') {
                        git credentialsId: 'jenkins', branch: 'main', url: ARGOCD_REPO

                        sh """
                        sed -i 's|image: .*|image: ${DOCKER_IMAGE}:${TAG}|' rollout.yaml
                        """

                        sh """
                        git add rollout.yaml
                        git commit -m "Update image tag to ${TAG}"
                        git push origin main
                        """
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
