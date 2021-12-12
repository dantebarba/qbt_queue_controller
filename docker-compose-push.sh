#!/bin/sh
export BUILD_VERSION=$(git describe --tags --dirty --always);
echo "VERSION IS: $BUILD_VERSION";
docker-compose build $@;
docker push dantebarba/qbt-queue-controller:latest;
docker push dantebarba/qbt-queue-controller:$BUILD_VERSION;
