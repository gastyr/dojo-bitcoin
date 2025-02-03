FROM python:3.12-slim-bullseye

# Instala UV usando a imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copia a aplicação para o container
COPY . .

# Usa o Python do sistema (apenas para containers)
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Instala as dependências usando UV
RUN uv sync --no-cache

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expõe a porta da API
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]