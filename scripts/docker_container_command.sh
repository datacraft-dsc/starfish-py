#!/bin/bash

# restart a named docker container

if [ -z $1 ]; then
    echo "Param #1 Please provide a docker container command"
    echo "docker_container_command <command> <container_search_name>"
    exit
fi

if [ -z $2 ]; then
    echo "Please provide a docker container name"
    echo "docker_container_command <command> <container_search_name>"
    exit
fi

DOCKER_ID=$(docker container ls | grep $2 | awk '{print $1}')
echo "Found container ${DOCKER_ID}"

if [ $1 == "ls" ]; then
    docker container $1 | grep $DOCKER_ID
    exit
fi

docker container $1 $DOCKER_ID
