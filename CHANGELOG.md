## Change Log

### Release v0.4.11

*   Add account balance and asset price check before purchasing an asset

### Release v0.4.9

*   Allow the watch event list to check for valid consumer address before starting agreement ( simple white listing on asset purchase).
*   Changed accounts to only support 'hosted' accounts for squid, but allow for local and host account setup.

### Release v0.4.8

*   Remove SquidAsset
*   Listing Data Price to use ocean tokens
*   Squid assets to only read the 'file' part of metadata
*   Squid agent to only return AssetBundle for the asset part of a listing

### Release v0.4.7

*   Supports: dex-2019-08-08
*   Supports: squid-py 0.6.15
*   New squid-agent method watch_provider_events

### Release v0.4.6
*   Fixed logging, so that only in test we setup the log level
*   Add a test to see if we have already purchased an asset in squid
*   Add MemoryAsset.save method

### Release v0.4.2

*   Include DDO as a module in package.

### Release v0.4.1

*   Improved asset classes
*   PD Test cases for file sharing

### Release v0.4.0

*   Supports: squid-py: v0.6.11
*   Supports: barge: dex-2019-06-17

### Release v0.3.0

*   Supports: squid-py: v0.6.5
*   Supports: barge: dex-2019-05-24