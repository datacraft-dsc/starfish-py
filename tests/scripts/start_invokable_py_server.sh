#!/bin/bash
docker rm /invokable-py -f
docker run \
    --detach \
    --publish 9090:9090  \
    --name invokable-py \
    docker.pkg.github.com/dex-company/invokable-py/testing:latest


