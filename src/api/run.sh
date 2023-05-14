#!/usr/bin/env bash

set -e

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=4 -b ${PROJECT_HOST}:${PROJECT_PORT} src.app:app