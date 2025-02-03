#!/bin/sh
# Busca o IP externo e exporta a variável EXTERNAL_IP
export EXTERNAL_IP=$(python3 -c "import urllib.request; print(urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf8').strip())")

# Opcional: loga a variável para debug
echo "Using API base URL: http://$EXTERNAL_IP"

# Inicia o servidor uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
