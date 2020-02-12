## Change Log

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
