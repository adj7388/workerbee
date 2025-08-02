#!/bin/bash

set -e

SERVICE_NAME=workerbee.service

echo "git pull"
git pull

echo "Writing Git commit hash to version/commit.txt"
git rev-parse HEAD > version/commit.txt

# Optional: generate human-readable version string
# echo "v1.4.2" > version/version.txt

echo "Restarting $SERVICE_NAME"
sudo systemctl restart $SERVICE_NAME

echo "Deploy complete. Current commit: $(cat version/commit.txt)"
