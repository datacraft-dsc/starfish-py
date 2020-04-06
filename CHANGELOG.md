## Change Log

### Release v0.8.7
+   README on develop/release life cycle
+   Fix docs build

### Release v0.8.6
+   Allow for local testing on nile network
+   create new starfish_tools.py script to provide basic tools
+   move wait_for_development.py to 'starfish_tools.py wait'

### Release v0.8.5
+   Remove test from package file
+   Release tools as scripts

### Release v0.8.4
+   Add contract article library to distribution
+   Refactor ContractManager
+   Add tool to add accounts and request ether from a faucet

### Release v0.8.3
+   Better DID validation and error reporting
+   add new functions in module utils.did: is_did, is_asset_did, asset_did_validate and did_validate
+   Read test contracts directly from barge
+   Tool to create a contract article json.gz file contracts on public networks
+   Tool to wait for development node to be built and contracts installed
+   Changed Account class to set the json key values on init, add new export, import, create features
+   Add request_ether_from_faucet method to DNetwork

### Release v0.8.2
+   Allow agent download and get asset to use an asset did or asset id
+   Change agent manager to pass an authentication_access dict instead of username, password
+   Add the ability to set a default agent in the agent manager list
+   Depreciated utils function `did_to_asset_id` to be replaced by `decode_to_asset_id`
+   General bug fixes

### Release v0.8.1

+   Allow users to pass a valid authentication token to the remote agent

### Release v0.8.0

+   Add AgentManager, to manage a list of agents with authorization details
+   Allow RemoteAgent to be created based on an agent_did, asset_did or DDO
+   Register a RemoteAgent using a DDO
+   Move DNetwork.connect to DNetwork.__init__

### Release v0.7.1

+   Fix badges on README

### Release v0.7.0

+   Large file upload and download using asset bundle and chunk of data assets
+   Direct Purchase contract using web3-py library only
+   Dex DID Registry contract
+   Dex Provenance contract
+   DNetwork class
+   Remove squid-py
+   Upgrade to the latest web3 library

### Release v0.6.6

+   better linting and module import order
+   Provenance
+   Split up register_asset and create_listing in agents
+   Changed squid to use register_asset_and_listing
+   change listing to pass the asset_did instead of the asset object

### Release v0.6.5

+   fix auth token to request via SurferAgentAdapter._http_client

### Release v0.6.4

+    Use the service 'auth' values to obtain a OAuth2 token
+    Implement invoke tests from surfer
+    Remove unused invoke agent and operation

### Release v0.6.3

+    Move the Job service over to Invoke service.

### Release v0.6.2

+    Rename services name metadata to meta

### Release v0.6.1

+    Improve adding and changing agent services.

### Release v0.6.0

+    Change the DID header id from :op: to :dep:
+    Change the DDO services from Ocean.xxx to DEP.xxx

### Release v0.5.8

+    Upgrade to use surfer 2020-01-31.2
+    Change the call to create a ddo using service descriptors

### Release v0.5.7

+    Allow for different response objects to use get_json(), json

### Release v0.5.6

+    Rename SurferAgent to RemoteAgent
+    Check the response object has the correct property before calling
+    Allow for different types or url building for the invoke & invoke jobs agent

### Release v0.5.5

+    Account class uses an agent_adapter property to convert to an agent_adapter_account
+    Minor fixes

### Release v0.5.3

+    Squid_py v0.7.1
+    barge/dex-2019-09-11

### Release v0.5.2

+    Code cleanup
+    Correct tox and barge tag errors

### Release v0.5.1

+    Add RemoteDataAsset
+    For compatibility upgrade to dex-2019-09-13

### Release v0.5.0

+    Upgrade to dex-2019-08-09
+    Removed FileAsset, MemoryAsset, RemoteAsset. Replaced with DataAsset
+    Cleanup documentation
+    Renamed Squid/Surfer Models to Squid/Surfer Agent Adapters

### Release v0.4.11

+    Add account balance and asset price check before purchasing an asset

### Release v0.4.9

+    Allow the watch event list to check for valid consumer address before starting agreement ( simple white listing on asset purchase).
+    Changed accounts to only support 'hosted' accounts for squid, but allow for local and host account setup.

### Release v0.4.8

+    Remove SquidAsset
+    Listing Data Price to use ocean tokens
+    Squid assets to only read the 'file' part of metadata
+    Squid agent to only return AssetBundle for the asset part of a listing

### Release v0.4.7

+    Supports: dex-2019-08-08
+    Supports: squid-py 0.6.15
+    New squid-agent method watch_provider_events

### Release v0.4.6

+    Fixed logging, so that only in test we setup the log level
+    Add a test to see if we have already purchased an asset in squid
+    Add MemoryAsset.save method

### Release v0.4.2

+    Include DDO as a module in package.

### Release v0.4.1

+    Improved asset classes
+    PD Test cases for file sharing

### Release v0.4.0

+    Supports: squid-py: v0.6.11
+    Supports: barge: dex-2019-06-17

### Release v0.3.0

+    Supports: squid-py: v0.6.5
+    Supports: barge: dex-2019-05-24
