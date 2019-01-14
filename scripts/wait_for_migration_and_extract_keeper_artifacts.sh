#!/bin/bash

RETRY_COUNT=0
CONTRACTS_READY=1

CONTRACT_FOLDER=artifacts

# make sure that we copy over the latest contrats, so remove any old folder
if [ -d ${CONTRACT_FOLDER} ]; then
    rm -rf ${CONTRACT_FOLDER}
fi

# receate empty
mkdir -p ${CONTRACT_FOLDER}

until [ ${CONTRACTS_READY} -eq 0 ] || [ ${RETRY_COUNT} -eq 120 ]; do
    KEEPER_CONTRACTS_DOCKER_ID=$(docker container ls | grep keeper-contracts | awk '{print $1}')
    docker cp ${KEEPER_CONTRACTS_DOCKER_ID}:/keeper-contracts/artifacts/. ./${CONTRACT_FOLDER}/
    CONTRACT_FILES=(${CONTRACT_FOLDER}/*.json)
    # test for the ready file and a json file
    if [ -f "${CONTRACT_FILES}" ] && [ -f "${CONTRACT_FOLDER}/ready" ]; then    
        CONTRACTS_READY=0
        break
    fi
    sleep 5
    let RETRY_COUNT=RETRY_COUNT+1
done

if [ ${CONTRACTS_READY} -eq 1 ]; then
    echo "Waited for more than ten minutes, but keeper contracts have not been migrated yet. Did you run an Ethereum RPC client and the migration script?"
    exit 1
fi

# docker cp ${KEEPER_CONTRACTS_DOCKER_ID}:/keeper-contracts/artifacts/. ./${CONTRACT_FOLDER}/
echo "copied over the following contracts:"
ls -1 ${CONTRACT_FOLDER}
