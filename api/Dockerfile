FROM python:3.12-slim-bullseye

# Instala UV usando a imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copia a aplicação para o container
COPY . .

# Usa o Python do sistema (apenas para containers)
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Instala as dependências usando UV
RUN uv sync --no-cache

# Expõe a porta da API
EXPOSE 8000

CMD ["sh", "-c", "EXTERNAL_IP=$(python -c \"import urllib.request; print(urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf8').strip())\") && echo External IP is: $EXTERNAL_IP && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
