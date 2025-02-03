#!/bin/sh
# Busca o IP externo
EXTERNAL_IP=$(curl -s https://checkip.amazonaws.com | tr -d '\n')

# Define a variável de ambiente para a URL base da API
export VITE_API_BASE_URL="http://$EXTERNAL_IP:8000"

# Opcionalmente, você pode logar a variável para debug
echo "Using API base URL: $VITE_API_BASE_URL"

# Gera o arquivo de configuração runtime
cat > /usr/share/nginx/html/config.js << EOF
window.runtimeConfig = {
  apiBaseUrl: "http://$EXTERNAL_IP:8000"
};
EOF

# Inicia o Nginx
exec nginx -g 'daemon off;'
