## Change Log

### Release v0.14.0
+   Add collection API to RemoteAgent

### Release v0.13.6
+   Add collection service to the list of services available for agents

### Release v0.13.5
+   convex ddo contract only excepts a full did string

### Release v0.13.4
+   Rebuild - same as v0.13.3

### Release v0.13.3
+   Fix ddo register, to accept quoted json text

### Release v0.13.2
+   Change convex network did register parameters to be the same as etherum network register

### Release v0.13.1
+   Cleanup Convex contracts
+   Allow for ethereum and convex network/accounts to be used from their module names

### Release v0.13.0
+   Use EthereumAccount and EtherumNetwork to access the ethereum network and contracts
+   Split the network into two types of block chain access: Convex and Ethereum
+   Use ConvexAccount and ConvexNetwork to access the convex network and contracts
+   Add auto deploy support for convex contracts

### Release v0.12.10
+   Fix key name error in AssetBundle class

### Release v0.12.9
+   Fix http_client bug

### Release v0.12.8
+   Allow to change the http_client on the Remote Agent

### Release v0.12.7
+   Moved http_client from a static value to a RemoteAgent/middleware object instance

### Release v0.12.6
+   Allow user to set the agent did

### Release v0.12.5
+   Change the DDO id ( DID ) to be generated from the hash of a DDO with an empty id

### Release v0.12.4
+   New Provenance format

### Release v0.12.2
+   Fix mongoquery to be installed as dependancy

### Release v0.12.1
+   Add a search for metadata assets information using the a dict filter
+   Only assign metadata values for data asset, when not set by the creator

### Release v0.12.0
+   Change BaseAsset class to be created from metadata text only
+   Add creation of provenance for asset registration

### Release v0.11.2
+   Allow to create/regiser remoete agents without a network connection
+   Fix get text bug in RemoteAgent Middleware

### Release v0.11.1
+   Add basic typing to API
+   Included the wait_for_surfer.sh, to wait during tests

### Release v0.11.0
+   Renamed network class from DNetwork to Network
+   Moved to using dex-chain for the block chain network contracts

### Release v0.10.0
+   Remove Network from agent classes

### Release v0.9.3
+   Allow to create remote agents with no Network object assigned

### Release v0.9.1
+   Bug fixes

### Release v0.9.0
+   Refactor resolver to main network object.  `resolve_agent` method resolves url/did to a ddo.

### Release v0.8.12
+   Removed 'id' from being published in the service record in a DDO
+   Ignored token request errors when trying to access an agent without the 'auth' service enabled

### Release v0.8.11
+   Allow to set metadata in tools store assets
+   Show asset metadata in downloaded assets
+   Add help commands to all of the sub commands in starfish_tools

### Release v0.8.10
+   Fix starfish_tools command line
+   Rename starfish_tools.py to starfish_tools

### Release v0.8.9
+   Move network method `load_development_contracts` to be called automatically on network object creation
+   Allow users to add an artifacts folder to load in different contract artifact files

### Release v0.8.8
+   Cleanup starfish tools
+   Asset store and download tool
+   Agent register and resolve tool
+   Account balance tool

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
