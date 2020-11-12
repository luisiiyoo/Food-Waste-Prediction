#!/bin/bash
APP_DIR='food-wasted_predictions'
GIT_REVISION='release'
BACKEND_PORT=5050

# Creating list of dependencies file to install (Python)
pipenv lock -r > requirements.txt

docker build -t \
    ${APP_DIR}:${GIT_REVISION} \
    -f ./Dockerfile \
    --build-arg GIT_REVISION=${GIT_REVISION} \
    --build-arg BACKEND_PORT=${BACKEND_PORT} \
    .
