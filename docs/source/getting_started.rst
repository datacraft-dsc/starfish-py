Getting Started
===============

.. _barge: https://github.com/DEX-Company/barge


Install the library
-------------------

    First you need to clone and download the latest version of starfish-py.
    Then you need to use ``virtualvenv`` to create a python enrivornment to work with.

    For example you can do something like this below:

    .. code-block:: console

        git clone https://github.com/DEX-Company/starfish-py.git
        cd starfish-py
        virtualvenv venv
        source venv/bin/activate
        pip install -r requirements_dev.txt

Run the unit tests
------------------

    You can run the unit tests without any external access to the Ocean Protocol Network, by running the command:

    .. code-block:: console

        pytest tests/unit


Startup a local ocean test node (``barge``)
-------------------------------------------

    Create the local testing environment using the barge_ repo.

    In a separate terminal session you need to clone and checkout the correct tagged
    version of ``barge`` repository, by doing the following:

    .. code-block:: console

        git clone https://github.com/DEX-Company/barge.git
        cd barge
        ./start_ocean.sh --no-brizo --no-pleuston --local-spree-node

    So you should now have two folders::

        myProjects/--|
                     |--> barge/
                     |--> starfish-py/


Copy keeper artifacts
---------------------

    A bash script is available to copy keeper artifacts into this file directly from a running docker image. This script needs to run in the root of the project.
    The script waits until the keeper contracts are deployed, and then copies the artifacts.

    using the following command:

    .. code-block:: console

        cd starfish-py
        ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh

    The artifacts contain the addresses of all the deployed contracts and their ABI definitions required to interact with them.


Run the full tests
------------------

    Once you have the local barge running. You now have a local Ocean Protocol Network stack running. You can now run the interegration tests by running the command:

    .. code-block:: console

        pytest tests/intergration

    or you can run the complete test suite by entering the command

    .. code-block:: console

        pytest tests
