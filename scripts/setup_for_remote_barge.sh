#!/bin/bash

# wait for barge artifact files

ARTIFACT_FOLDER="artifacts"
REMOTE_BARGE=http://52.187.164.74:8090
if [ ! -z $1 ]; then
    REMOTE_BARGE=$1
fi

if [ -d $ARTIFACT_FOLDER ]; then
    rm -rf $ARTIFACT_FOLDER
fi

mkdir $ARTIFACT_FOLDER
cd $ARTIFACT_FOLDER
wget -r -nd ${REMOTE_BARGE}/api/v1/ferry/barge/artifacts
