git clone https://github.com/DEX-Company/barge.git

DOCKER_RETRY=1
BARGE_DELAY=240
until [ $DOCKER_RETRY -gt 10 ]; do
    cd barge
    git checkout dex-2019-06-17
    ./start_ocean.sh --no-brizo --no-pleuston --local-spree-node 2>&1 > barge.log &
    cd ..
    echo "sleeping for $BARGE_DELAY seconds"
    sleep $BARGE_DELAY
    echo "Waiting for keeper contracts to be build"
    ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
    SURFER_FAIL=`egrep 'ocean_surfer.*exited' barge/barge.log`
    if [ -z "$SURFER_FAIL" ]; then
        DOCKER_RETRY=100
        echo "surfer is running"
    else
        echo "surfer failed to startup retry No. ${DOCKER_RETRY}"
        echo "Stopping all docker containers"
        docker kill $(docker ps -a -q)
        sudo systemctl restart docker
        echo "running docker containers"
        docker container ls
        ((DOCKER_RETRY++))
        BARGE_DELAY=60
    fi
    echo "------------------------ Start Barge Log -----------------------"
    cat barge/barge.log
    echo "------------------------ End Barge Log -------------------------"
done
