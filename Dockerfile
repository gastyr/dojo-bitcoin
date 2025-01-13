FROM python:3.12-slim-bullseye

# Instala UV usando a imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copia a aplicação para o container
COPY . /app

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências usando UV
RUN uv sync --frozen --no-cache

# Expõe a porta da API
EXPOSE 8000

# Roda a aplicação usando uvicorn
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]