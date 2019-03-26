#!/bin/bash

CONTAINER_IMAGE="registry.gitlab.com/chariot-h2020/chariot-northbound-dispatcher"
CI_COMMIT_TAG="v0.3.0"

docker build --cache-from $CONTAINER_IMAGE:latest --tag $CONTAINER_IMAGE:$CI_COMMIT_TAG --tag $CONTAINER_IMAGE:latest -f ./Dockerfile.dispatcher .
docker build --cache-from $CONTAINER_IMAGE/api:latest --tag $CONTAINER_IMAGE/api:$CI_COMMIT_TAG --tag $CONTAINER_IMAGE/api:latest .
