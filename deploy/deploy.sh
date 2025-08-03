#!/bin/bash

set -e

SERVICE_NAME=workerbee.service
COMMIT_HASH_FILE=commit.txt

echo "Writing Git commit hash to commit.txt"
git rev-parse HEAD > $COMMIT_HASH_FILE

# Optional: generate human-readable version string
# echo "v1.4.2" > version/version.txt

echo "Copy $SERVICE_NAME to /etc/systemd/system"
sudo cp deploy/$SERVICE_NAME /etc/systemd/system

echo "Reloading systemd daemon"
sudo systemctl daemon-reload
echo "Restarting $SERVICE_NAME"
sudo systemctl restart $SERVICE_NAME

echo "Deploy complete. Current commit: $(cat $COMMIT_HASH_FILE)"
