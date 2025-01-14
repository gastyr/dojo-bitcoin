FROM python:3.12-slim-bullseye

# Instala UV usando a imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copia a aplicação
COPY . .

# Cria o ambiente virtual e instala dependências
RUN uv venv

# Expõe a porta da API
EXPOSE 8000

# Roda a aplicação usando uvicorn do ambiente virtual
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]