git clone https://github.com/DEX-Company/barge.git

RETRY=0
until [ $RETRY -gt 5 ]; do
    cd barge
    git checkout dex-2019-06-17
    ./start_ocean.sh --no-brizo --no-pleuston --local-spree-node 2>&1 > barge.log &
    cd ..
    sleep 240
    echo "Waiting for keeper contracts to be build"
    ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
    SURFER_FAIL=`grep 'ocean_surfer.*exited' barge/barge.log`
    echo $SURFER_FAIL
    if [ -z "$SURFER_FAIL" ]; then
        RETRY=10
        echo "surfer is running"
    else
        echo "surfer failed to startup"
        echo "Stoping all docker containers"
        docker kill $(docker ps -a -q)
        ((RETRY++))
    fi
done
./scripts/wait_for_surfer.sh http://localhost:8080
