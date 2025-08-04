#!/bin/bash
set -e

SERVICE_NAME="workerbee.service"
ENV_FILE="/etc/workerbee.env"
COMMIT_HASH_FILE="commit.txt"
SITE_NAME="alanjohnston.me"
AVAILABLE="/etc/nginx/sites-available/$SITE_NAME"
ENABLED="/etc/nginx/sites-enabled/$SITE_NAME"

if [ ! -f "$ENV_FILE" ]; then
    echo "Missing $ENV_FILE. Please create it before deploying."
    echo "See $ENV_FILE.example."
    exit 1
fi

echo "Copying $AVAILABLE"
sudo cp "deploy/$SITE_NAME" "$AVAILABLE"

echo "Symlink to sites-available"
sudo ln -sfn "$AVAILABLE" "$ENABLED"

echo "Testing nginx.conf"
sudo nginx -t

echo "Copy $SERVICE_NAME to /etc/systemd/system"
sudo cp "deploy/$SERVICE_NAME" "/etc/systemd/system"

echo "Reloading systemd daemon"
sudo systemctl daemon-reload

echo "Restarting Nginx"
sudo systemctl restart nginx.service

echo "Restarting $SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "Writing Git commit hash to $COMMIT_HASH_FILE"
git rev-parse HEAD > "$COMMIT_HASH_FILE"

echo "Deploy complete. Current commit: $(cat "$COMMIT_HASH_FILE")"
echo "That is all"
