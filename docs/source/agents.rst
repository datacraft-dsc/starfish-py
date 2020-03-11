Starfish Agents
===============

There are three type of Starfish agents.

MemoryAgent
    The memory agent provides almost the same functionallity as the other agents.
    But does all it's work in memory and does not interact with any external service, or network.

SurferAgent
    The Surfer agent allows you to register an asset and upload/download asset data.

    To do this the Surfer agent, connects to the Surfer service and registers the asset
    using it's metadata.

    The returned id will contain a `Surfer_DID/asset_id` combination. Where the first item is the Surfer DID, and the second item
    is the Asset id.
