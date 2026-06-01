pipeline {
    agent any

    environment {
        PROJETO        = 'hubkealex-v2'
        DEPLOY_PATH    = '/var/jenkins_home/apps/hubkealex-v2'
        GIT_REPO       = 'https://github.com/kealabs-ai/hubkealabs-v2.git'
        GIT_BRANCH     = 'master'
        DOCKER         = '/var/jenkins_home/docker'
        DOCKER_COMPOSE = '/var/jenkins_home/docker-compose'
    }

    stages {

        // ── 1. CHECKOUT ───────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ── 2. PREPARAR AMBIENTE ──────────────────────────────────────────
        stage('Prepare') {
            steps {
                sh '''
                    set -e
                    mkdir -p $DEPLOY_PATH
                    cd $DEPLOY_PATH

                    if [ -d ".git" ]; then
                        git fetch origin
                        git reset --hard origin/$GIT_BRANCH
                    else
                        git clone -b $GIT_BRANCH $GIT_REPO .
                    fi

                    echo "  ✔ Repositório atualizado em $DEPLOY_PATH"
                '''
            }
        }

        // ── 3. GARANTIR DOCKER BUILDX ─────────────────────────────────────
        stage('Ensure Buildx') {
            steps {
                sh '''
                    BUILDX_PATH="/var/jenkins_home/.docker/cli-plugins/docker-buildx"
                    if [ ! -f "$BUILDX_PATH" ]; then
                        echo "Instalando docker-buildx..."
                        mkdir -p /var/jenkins_home/.docker/cli-plugins
                        curl -fsSL "https://github.com/docker/buildx/releases/download/v0.17.1/buildx-v0.17.1.linux-amd64" \
                             -o "$BUILDX_PATH"
                        chmod +x "$BUILDX_PATH"
                        echo "  ✔ buildx instalado"
                    else
                        echo "  ✔ buildx já presente"
                    fi
                '''
            }
        }

        // ── 4. BUILD E DEPLOY ─────────────────────────────────────────────
        stage('Deploy') {
            steps {
                sh '''
                    set -e
                    cd $DEPLOY_PATH

                    echo "▶ Derrubando stack anterior..."
                    $DOCKER_COMPOSE -f docker-compose.yml -p $PROJETO down --remove-orphans 2>/dev/null || true

                    echo "▶ Build e subida dos containers..."
                    $DOCKER_COMPOSE -f docker-compose.yml -p $PROJETO up -d --build

                    echo "✅ Deploy concluído"
                '''
            }
        }

        // ── 5. RELOAD NGINX ───────────────────────────────────────────────
        stage('Reload Nginx') {
            steps {
                sh '''
                    $DOCKER exec nginx nginx -t && $DOCKER exec nginx nginx -s reload
                    echo "  ✔ Nginx recarregado"
                '''
            }
        }

        // ── 6. HEALTH CHECK ───────────────────────────────────────────────
        stage('Health Check') {
            steps {
                sh '''
                    echo "▶ Aguardando containers subirem (10s)..."
                    sleep 10

                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
                        --max-time 5 \
                        https://srv1023256.hstgr.cloud/v2/lex/health || echo "000")

                    if [ "$STATUS" = "200" ]; then
                        echo "  ✔ /v2/lex/health → OK"
                    else
                        echo "  ✘ /v2/lex/health → HTTP $STATUS"
                        exit 1
                    fi
                '''
            }
        }

    }

    post {
        success {
            echo '✅ Deploy HubKealex v2 realizado com sucesso!'
        }
        failure {
            echo '❌ Falha no deploy HubKealex v2!'
        }
        always {
            node('built-in') {
                sh '''
                    echo "▶ Estado final dos containers:"
                    /var/jenkins_home/docker ps --filter "name=hubkealex-v2" || true
                '''
            }
        }
    }
}
