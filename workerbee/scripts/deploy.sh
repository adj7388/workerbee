#!/bin/bash

set -e

SERVICE_NAME=workerbee.service

echo "Writing Git commit hash to commit.txt"
git rev-parse HEAD > workerbee/commit.txt

# Optional: generate human-readable version string
# echo "v1.4.2" > version/version.txt

echo "Restarting $SERVICE_NAME"
sudo systemctl restart $SERVICE_NAME

echo "Deploy complete. Current commit: $(cat workerbee/commit.txt)"
