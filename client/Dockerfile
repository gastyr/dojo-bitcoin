# Stage 1: Develop stage
FROM node:lts-slim AS develop-stage

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install Quasar CLI
RUN npm -g @quasar/cli

# Copy source files
COPY . .

# Stage 2: Build stage
FROM develop-stage as build-stage

RUN npm install

# Build Quasar app
RUN quasar build

# Stage 2: Production server
FROM nginx:stable-alpine

# Copy built assets from builder
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html

# Copy custom nginx config (if needed)
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/nginx.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port and start server
EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]