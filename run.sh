#!/bin/bash
APP_DIR='food-wasted_predictions'
GIT_REVISION='release'
BACKEND_PORT=5050

docker stop ${APP_DIR}-${GIT_REVISION}
docker rm ${APP_DIR}-${GIT_REVISION}

docker run -dit \
        -p ${BACKEND_PORT}:${BACKEND_PORT} \
        --name ${APP_DIR}-${GIT_REVISION} \
        ${APP_DIR}:${GIT_REVISION}

GET_CONTAINER_ID_COMMAND="docker ps -aqf name=${APP_DIR}-${GIT_REVISION}"
CONTAINER_ID=$(eval "${GET_CONTAINER_ID_COMMAND}")
docker logs -f ${CONTAINER_ID}

# Remove all untagged images: docker rmi -f $(docker images | grep "^<none>" | awk "{print $3}")
# Execute the container on terminal: docker exec -it food-wasted_predictions-release /bin/bash
# Show all the containers: docker ps -a
# Show all the images: docker images

