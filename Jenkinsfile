pipeline {
    agent any

    environment {
        VPS_HOST   = 'srv1023256.hstgr.cloud'
        VPS_USER   = 'root'
        DEPLOY_DIR = '/opt/hubkealex-v2'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/kealabs-ai/hubkealabs-v2.git'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'vps-credentials', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS')]) {
                    sh """
                        sshpass -p '${SSH_PASS}' ssh -o StrictHostKeyChecking=no ${SSH_USER}@${VPS_HOST} 'mkdir -p ${DEPLOY_DIR}'

                        sshpass -p '${SSH_PASS}' rsync -az --delete \
                            --exclude='.git' \
                            --exclude='.qodo' \
                            -e 'ssh -o StrictHostKeyChecking=no' \
                            ./ ${SSH_USER}@${VPS_HOST}:${DEPLOY_DIR}/

                        sshpass -p '${SSH_PASS}' ssh ${SSH_USER}@${VPS_HOST} '
                            cd ${DEPLOY_DIR} &&
                            docker compose down --remove-orphans &&
                            docker compose build --no-cache &&
                            docker compose up -d
                        '
                    """
                }
            }
        }

        stage('Reload Nginx') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'vps-credentials', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS')]) {
                    sh "sshpass -p '${SSH_PASS}' ssh ${SSH_USER}@${VPS_HOST} 'nginx -t && systemctl reload nginx'"
                }
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 5'
                sh "curl -f https://${VPS_HOST}/v2/lex/health || exit 1"
            }
        }
    }

    post {
        failure {
            echo 'Deploy falhou. Verifique os logs acima.'
        }
        success {
            echo 'Deploy concluído com sucesso.'
        }
    }
}
