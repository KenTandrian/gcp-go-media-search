# Stage 1: Build the React application
FROM node:22-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package manager files
COPY package.json pnpm-lock.yaml ./

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install

# Copy the rest of the application source code
COPY . .

# Build the application
RUN pnpm build

# Stage 2: Serve the application with Nginx
FROM nginx:1.29-alpine

# Copy the build output from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the Nginx configuration template and startup script
COPY nginx.conf.template /etc/nginx/conf.d/nginx.conf.template
COPY scripts/start-nginx.sh /start-nginx.sh

# Make the startup script executable
RUN chmod +x /start-nginx.sh

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Use the script to start Nginx
CMD ["/start-nginx.sh"]
