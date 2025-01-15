# Etapa 1: Build
FROM node:22-alpine AS build

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos essenciais para instalação
COPY package.json package-lock.json ./ 

# Instala as dependências do projeto
RUN npm install

# Copia todo o código para o contêiner
COPY . .

# Executa o processo de build do Vite
RUN npm run build

# Etapa 2: Servidor Nginx
FROM nginx:stable-alpine

# Remove o arquivo de configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia o arquivo de configuração personalizado para o Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos do build do Vite para o diretório de publicação do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expõe a porta padrão do Nginx
EXPOSE 80

# Define o comando de entrada para o contêiner
CMD ["nginx", "-g", "daemon off;"]
