git clone https://github.com/DEX-Company/barge.git
cd barge
git checkout dex-2019-06-17
bash -x start_ocean.sh --no-brizo --no-pleuston --local-spree-node 2>&1 > start_ocean.log &
cd ..
sleep 240
scripts/wait_for_migration_and_extract_keeper_artifacts.sh