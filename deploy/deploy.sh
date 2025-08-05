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

echo "Copying $SITE_NAME to $AVAILABLE"
sudo cp "deploy/$SITE_NAME" "$AVAILABLE"

echo "Symlink $ENABLED to $AVAILABLE"
sudo ln -sfn "$AVAILABLE" "$ENABLED"

sudo nginx -t

echo "Copy $SERVICE_NAME to /etc/systemd/system"
sudo cp "deploy/$SERVICE_NAME" "/etc/systemd/system"

echo "Reloading systemd daemon"
sudo systemctl daemon-reload

echo "Writing Git commit hash to $COMMIT_HASH_FILE"
git rev-parse HEAD > "$COMMIT_HASH_FILE"

echo "Restarting $SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "Reloading Nginx"
sudo systemctl reload nginx

echo "Deploy complete. Current commit: $(cat "$COMMIT_HASH_FILE")"
echo "That is all"
