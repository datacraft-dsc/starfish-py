#!/bin/bash

# wait for surfer to respond

SURFER_URL=$1
RETRY_COUNT=0
SURFER_READY=0

if [ -z $SURFER_URL ]; then
    SURFER_URL="http://localhost:8080"
fi

CURL_CMD="curl -w httpcode=%{http_code}"

# See retry options https://stackoverflow.com/a/42873372/845843
CURL_MAX_CONNECTION_TIMEOUT="--retry-max-time 10 --retry-connrefused --retry 10 "


echo "Waiting for Surfer to be up at $SURFER_URL"
until [ ${SURFER_READY} -eq 1 ] || [ ${RETRY_COUNT} -eq 120 ]; do

    # perform curl operation
    CURL_RETURN_CODE=0
    CURL_OUTPUT=`${CURL_CMD} ${CURL_MAX_CONNECTION_TIMEOUT} ${SURFER_URL} 2> /dev/null` || CURL_RETURN_CODE=$?

    # test for the ready file and a json file
    if [ ${CURL_RETURN_CODE} -eq 0 ]; then
        SURFER_READY=1
        echo "connection success"
        break
    else
        echo "Connection failed with return code - ${CURL_RETURN_CODE}"
    fi
    sleep 5
    let RETRY_COUNT=RETRY_COUNT+1
done

if [ ${SURFER_READY} -eq 0 ]; then
    echo "Waited for more than ten minutes for surfer to start"
    exit 1
fi
