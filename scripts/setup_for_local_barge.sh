#!/bin/bash

BARGE_DELAY=120

git clone https://github.com/DEX-Company/barge.git
cd barge
git checkout tags/dex-2019-09-03
./start_ocean.sh --no-brizo --no-pleuston --local-spree-node 2>&1 > barge.log &
cd ..
echo "sleeping for $BARGE_DELAY seconds"
sleep $BARGE_DELAY
echo "Waiting for keeper contracts to be build"
./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
