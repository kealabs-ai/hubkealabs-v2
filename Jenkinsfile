pipeline {
    agent any

    environment {
        VPS_HOST        = 'srv1023256.hstgr.cloud'
        VPS_USER        = 'root'
        DEPLOY_DIR      = '/opt/hubkealex-v2'
        SSH_CREDENTIALS = 'vps-ssh-key'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            steps {
                sshagent(credentials: [SSH_CREDENTIALS]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} '
                            mkdir -p ${DEPLOY_DIR}
                        '

                        rsync -az --delete \
                            --exclude='.git' \
                            --exclude='.qodo' \
                            ./ ${VPS_USER}@${VPS_HOST}:${DEPLOY_DIR}/

                        ssh ${VPS_USER}@${VPS_HOST} '
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
                sshagent(credentials: [SSH_CREDENTIALS]) {
                    sh """
                        ssh ${VPS_USER}@${VPS_HOST} 'nginx -t && systemctl reload nginx'
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                sh "sleep 5"
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
