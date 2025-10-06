#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Substitute environment variables in the nginx configuration template
envsubst '${BACKEND_HOST}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Start Nginx in the foreground
exec nginx -g 'daemon off;'
