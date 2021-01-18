#!/bin/bash
docker rm /invokable-py -f
docker run \
    --detach \
    --publish 9090:9090  \
    --name invokable-py \
    docker.pkg.github.com/datacraft-dsc/invokable-py/invokable-py:latest


