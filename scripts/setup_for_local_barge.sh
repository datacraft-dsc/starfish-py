#!/bin/bash

BARGE_DELAY=120

git clone https://github.com/DEX-Company/barge.git
cd barge
git checkout develop
./start_ocean.sh --no-brizo --no-surfer --no-koi --no-aquarius --no-dashboard --no-secret-store --local-spree-node 2>&1 > barge.log &
cd ..
echo "sleeping for $BARGE_DELAY seconds"
sleep $BARGE_DELAY
echo "Waiting for keeper contracts to be build"
./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
