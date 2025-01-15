FROM python:3.12-slim-bullseye

# Instala UV usando a imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copia apenas os arquivos necessários para o simulador
COPY . .
COPY ../pyproject.toml .
COPY ../.python-version .

# Usa o Python do sistema (apenas para containers)
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Instala as dependências usando UV
RUN uv sync --no-cache

# Script que aguarda o bitcoin node e executa a simulação
CMD ["python3", "block_simulator.py"]