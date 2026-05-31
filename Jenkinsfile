pipeline {
    agent any

    environment {
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
                sh """
                    rsync -az --delete \
                        --exclude='.git' \
                        --exclude='.qodo' \
                        ./ ${DEPLOY_DIR}/

                    cd ${DEPLOY_DIR} &&
                    docker compose down --remove-orphans &&
                    docker compose build --no-cache &&
                    docker compose up -d
                """
            }
        }

        stage('Reload Nginx') {
            steps {
                sh 'sudo nginx -t && sudo systemctl reload nginx'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 5'
                sh 'curl -f https://srv1023256.hstgr.cloud/v2/lex/health || exit 1'
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
