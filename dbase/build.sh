rm -rf venv
#!/usr/bin/env bash
set -e
IMAGE_NAME="pwapp"
TAG="latest"
echo "Building Docker image: ${IMAGE_NAME}:${TAG}"
docker build -t "${IMAGE_NAME}:${TAG}" .
