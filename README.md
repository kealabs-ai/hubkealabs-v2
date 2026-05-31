# HubKealex v2

Microserviço Python (FastAPI) com endpoints em `/v2/lex`.

## Endpoints

| Método | Path              | Descrição          |
|--------|-------------------|--------------------|
| GET    | /v2/lex/health    | Health check       |
| GET    | /v2/lex/test      | Endpoint de teste  |

## Setup na VPS (primeira vez)

```bash
# 1. Criar a rede Docker compartilhada (se ainda não existir)
docker network create kealabs-net

# 2. Clonar o repositório
git clone <repo-url> /opt/hubkealex-v2
cd /opt/hubkealex-v2

# 3. Subir o container
docker compose up -d --build

# 4. Adicionar o bloco do nginx/location.conf dentro do server block existente
#    em /etc/nginx/sites-available/srv1023256.hstgr.cloud
#    e recarregar:
nginx -t && systemctl reload nginx
```

## Jenkins

- Credencial SSH necessária com ID: `vps-ssh-key`
- O pipeline faz: checkout → rsync → docker compose up → reload nginx → health check
