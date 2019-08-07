Starfish Agents
===============

There are three type of Starfish agents.

MemoryAgent
    The memory agent provides almost the same functionallity as the other agents.
    But does all it's work in memory and does not interact with any external service, or network.

SquidAgent
    The Squid agent allows the user to register an asset directly on the Ocean Protocol Network.

    You can only regsiter URL's or file name's using the SquidAgent.

    The reason for the limitation that you can not register a DataAsset with no data,
    is that you will have to also create seperate service called `Brizo` to enable access
    for purchased asset data.

    The data will then need to be stored on a cloud data storage server where Brizo can have access to the data.

    To setup the full data storage service you need to do the following:

    1. Setup a storage area such as Amazon or Azure storage.
    2. Place your asset data in this storage.
    3. Setup a Brizo server to provide read access to the asset files on the cloud storage server.

    When you register an asset for use with Brizo storage, you just need to pass the URL or filename
    of the file on the cloud storage server.

    After registering an asset with Squid, you will get a unique DID that can be discovered and
    resolved on the Ocean Network.

SurferAgent
    The Surfer agent allows you to register an asset and upload/download asset data.

    To do this the Surfer agent, connects to the Surfer service and registers the asset
    using it's metadata.

    The returned asset DID or listing id is different to the registered asset in SquidAgent. Instead of a single DID, the
    returned id will contain a `Surfer_DID/asset_id` combination. Where the first item is the Surfer DID, and the second item
    is the Asset id.


Agent Comparison
----------------

SquidAgent and SurferAgent work in different ways and both have their benefits and disadvantges.

SquidAgent
^^^^^^^^^^

Benefits
    * Register an asset on the Ocean Protocol Network and get a unique id
    * Recorded on the Ocean Protocol Network

Drawbacks
    * Need small amount of ether to register an asset
    * Can only pass a URL or filename for registeration
    * Need to maintain a Brizo service & cloud storage to provide asset downloads.
    * Slow to register an asset, since it requires block chain transaction.


SurferAgent
^^^^^^^^^^^

Benefits
    * Register an asset does not cost any ether.
    * Can upload/download asset data with Surfer.
    * Fast to register asset

Drawbacks
    * Registered asset is not on the Ocean Protocol Network.



