Starfish Agents
===============

There are three type of Starfish agents.

MemoryAgent
    The memory agent provides almost the same functionallity as the other agents.
    But does all it's work in memory and does not interact with any external service, or network.

SquidAgent
    The Squid agent allows the user to register an asset directly on the Ocean Protocol Network.

    You can only regsiter URL's or file name's using the SquidAgent.

    The reason is that you will have to also create seperate service called `Brizo` to enable access
    for purchased asset data.

    To do this you need to do the following:

    1. Setup a storage area such as Amazon or Azure storage.
    2. Place your asset data in this storage.
    3. Setup a Brizo server to provide access to the asset files.

    When you register an asset for use with Brizo you will then need to provide the
    Brizo URL when registering an asset.

    After registering an asset with Squid, you will get a unique DID that can be discovered and
    resolved on the Ocean Network.

SurferAgent
    The Surfer agent allows you to register an asset and upload/download asset data.
    To do this the Surfer agent, connects to the Surfer service and registers the asset
    using it's metadata.

    The returned link is different to the registered asset in SquidAgent. Instead of a single DID, the
    returned link will contain a `DID/id`. Where the first item is the Surfer DID, and the second item
    is the Asset id.


Agent Comparison
----------------

SquidAgent and SurferAgent work in different ways and both have their benefits and disadvantges.

SquidAgent
^^^^^^^^^^


Benefits
    * Register an asset on the Network and get a unique id

Drawbacks
    * Need small amount of ether to register an asset
    * Can only pass a URL or filename for registeration
    * Need to maintain a Brizo service & cloud storage to provide asset downloads.


SurferAgent
^^^^^^^^^^^

Benefits
    * Register an asset does not cost any ether.
    * Can upload/download asset data with Surfer.

Drawbacks
    * Registered asset is not on the Network.



