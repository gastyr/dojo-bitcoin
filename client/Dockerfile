# Stage 1: Build application
FROM node:lts-slim AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies with clean cache
RUN npm install

# Copy source files
COPY . .

# Run quasar prepare with full project structure
RUN npx quasar prepare

RUN npm install

# Build Quasar app
RUN quasar build

# Stage 2: Production server
FROM nginx:stable-alpine

# Copy built assets from builder
COPY --from=builder /app/dist/spa /usr/share/nginx/html

# Copy custom nginx config (if needed)
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/nginx.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port and start server
EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]