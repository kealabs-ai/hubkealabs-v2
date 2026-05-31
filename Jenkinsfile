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
                    mkdir -p ${DEPLOY_DIR}
                    cp -r . ${DEPLOY_DIR}/
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v ${DEPLOY_DIR}:${DEPLOY_DIR} \
                        -w ${DEPLOY_DIR} \
                        docker/compose:latest \
                        -f ${DEPLOY_DIR}/docker-compose.yml \
                        -p hubkealex-v2 down --remove-orphans
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v ${DEPLOY_DIR}:${DEPLOY_DIR} \
                        -w ${DEPLOY_DIR} \
                        docker/compose:latest \
                        -f ${DEPLOY_DIR}/docker-compose.yml \
                        -p hubkealex-v2 up -d --build
                """
            }
        }

        stage('Reload Nginx') {
            steps {
                sh 'docker exec nginx nginx -t && docker exec nginx nginx -s reload'
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
