#!/bin/bash

set -e

SERVICE_NAME=workerbee.service
ENV_FILE=/etc/workerbee.env
COMMIT_HASH_FILE=commit.txt
NGINX_CONF=nginx.conf


if [ ! -f "$ENV_FILE" ]; then
    echo "Missing $ENV_FILE. Please create it before deploying."
    echo "See $ENV_FILE.example."
    exit 1
fi

echo "Copying $NGINX_CONF to /etc/nginx"
sudo cp deploy/$NGINX_CONF /etc/nginx

echo "Testing $NGINX_CONF"
sudo nginx -t -c /etc/nginx/$NGINX_CONF

echo "Copy $SERVICE_NAME to /etc/systemd/system"
sudo cp deploy/$SERVICE_NAME /etc/systemd/system

echo "Reloading systemd daemon"
sudo systemctl daemon-reload

echo "Restarting Nginx"
sudo systemctl restart nginx.service

echo "Restarting $SERVICE_NAME"
sudo systemctl restart $SERVICE_NAME

echo "Writing Git commit hash to commit.txt"
git rev-parse HEAD > $COMMIT_HASH_FILE

# Optional: generate human-readable version string
# echo "v1.4.2" > version/version.txt

echo "Deploy complete. Current commit: $(cat $COMMIT_HASH_FILE)"
echo "That is all"