#!/bin/sh
# Busca o IP externo
EXTERNAL_IP=$(curl -s https://checkip.amazonaws.com | tr -d '\n')

# Opcionalmente, você pode logar a variável para debug
echo "Using API base URL: http://$EXTERNAL_IP"

# Inicia o servidor
exec uvicorn app.main:app --host 0.0.0.0 --port 8000