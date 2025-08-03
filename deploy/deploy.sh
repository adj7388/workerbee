#!/bin/bash

set -e

SERVICE_NAME=workerbee.service
ENV_FILE=/etc/workerbee.env
COMMIT_HASH_FILE=commit.txt

if [ ! -f "$ENV_FILE" ]; then
    echo "Missing $ENV_FILE. Please create it before deploying."
    exit 1
fi

# Copy service file to /etc/systemd/system
echo "Copy $SERVICE_NAME to /etc/systemd/system"
sudo cp deploy/$SERVICE_NAME /etc/systemd/system

echo "Writing Git commit hash to commit.txt"
git rev-parse HEAD > $COMMIT_HASH_FILE

# Optional: generate human-readable version string
# echo "v1.4.2" > version/version.txt

echo "Reloading systemd daemon"
sudo systemctl daemon-reload
echo "Restarting $SERVICE_NAME"
sudo systemctl restart $SERVICE_NAME

echo "Deploy complete. Current commit: $(cat $COMMIT_HASH_FILE)"
echo "That is all"