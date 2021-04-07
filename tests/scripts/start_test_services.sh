#!/bin/bash

echo "Start surfer"
docker run \
    --detach \
    --publish 3030:3030 \
    docker.pkg.github.com/datacraft-dsc/surfer/surfer:latest


echo "Start invokable-py"
docker rm /invokable-py -f
docker run \
    --detach \
    --publish 9090:9090  \
    --name invokable-py \
    docker.pkg.github.com/datacraft-dsc/invokable-py/invokable-py:latest


echo "Wait for surfer"
docker run --network host docker.pkg.github.com/datacraft-dsc/surfer/surfer:latest ./scripts/wait_for_surfer.sh

echo "All test services are ready"
