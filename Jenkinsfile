pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/kealabs-ai/hubkealabs-v2.git'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $WORKSPACE:$WORKSPACE \
                        -w $WORKSPACE \
                        docker/compose:latest \
                        -f $WORKSPACE/docker-compose.yml \
                        -p hubkealex-v2 down --remove-orphans 2>/dev/null || true

                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $WORKSPACE:$WORKSPACE \
                        -w $WORKSPACE \
                        docker/compose:latest \
                        -f $WORKSPACE/docker-compose.yml \
                        -p hubkealex-v2 up -d --build
                '''
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
