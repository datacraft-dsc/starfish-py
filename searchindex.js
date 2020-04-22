Search.setIndex({docnames:["agents","classes/account","classes/agent","classes/agent/agent_base","classes/agent/memory_agent","classes/agent/remote_agent","classes/asset","classes/asset/asset_base","classes/asset/bundle_asset","classes/asset/data_asset","classes/asset/module","classes/asset/operation_asset","classes/dnetwork","classes/job","classes/job/job","classes/job/job_base","classes/listing","classes/listing/listing","classes/listing/listing_base","classes/provenance","classes/purchase","classes/purchase/purchase","classes/purchase/purchase_base","getting_started","index","register_asset_remote_agent","starfish_tools"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":2,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,sphinx:56},filenames:["agents.rst","classes/account.rst","classes/agent.rst","classes/agent/agent_base.rst","classes/agent/memory_agent.rst","classes/agent/remote_agent.rst","classes/asset.rst","classes/asset/asset_base.rst","classes/asset/bundle_asset.rst","classes/asset/data_asset.rst","classes/asset/module.rst","classes/asset/operation_asset.rst","classes/dnetwork.rst","classes/job.rst","classes/job/job.rst","classes/job/job_base.rst","classes/listing.rst","classes/listing/listing.rst","classes/listing/listing_base.rst","classes/provenance.rst","classes/purchase.rst","classes/purchase/purchase.rst","classes/purchase/purchase_base.rst","getting_started.rst","index.rst","register_asset_remote_agent.rst","starfish_tools.rst"],objects:{"starfish.DNetwork":{contract_names:[12,1,1,""],find_network_name_from_id:[12,1,1,""],get_contract:[12,1,1,""],get_ether_balance:[12,1,1,""],get_provenace_event_list:[12,1,1,""],get_token_balance:[12,1,1,""],is_token_sent:[12,1,1,""],load_development_contracts:[12,1,1,""],name:[12,1,1,""],register_did:[12,1,1,""],register_provenace:[12,1,1,""],request_ether_from_faucet:[12,1,1,""],request_test_tokens:[12,1,1,""],resolve_agent:[12,1,1,""],resolve_did:[12,1,1,""],send_ether:[12,1,1,""],send_token:[12,1,1,""],send_token_and_log:[12,1,1,""],url:[12,1,1,""],web3:[12,1,1,""]},"starfish.account":{Account:[1,0,1,""]},"starfish.account.Account":{address:[1,1,1,""],as_checksum_address:[1,1,1,""],create:[1,1,1,""],export_key:[1,1,1,""],export_key_value:[1,1,1,""],import_key:[1,1,1,""],import_key_value:[1,1,1,""],is_address_equal:[1,1,1,""],is_password:[1,1,1,""],is_valid:[1,1,1,""],key_value:[1,1,1,""],load_from_file:[1,1,1,""],password:[1,1,1,""],save_to_file:[1,1,1,""],set_password:[1,1,1,""],sign_transaction:[1,1,1,""]},"starfish.agent":{MemoryAgent:[4,0,1,""],RemoteAgent:[5,0,1,""]},"starfish.agent.MemoryAgent":{consume_asset:[4,1,1,""],create_listing:[4,1,1,""],get_asset_purchase_ids:[4,1,1,""],get_listing:[4,1,1,""],is_access_granted_for_asset:[4,1,1,""],purchase_asset:[4,1,1,""],purchase_wait_for_completion:[4,1,1,""],register_asset:[4,1,1,""],search_listings:[4,1,1,""],update_listing:[4,1,1,""],validate_asset:[4,1,1,""]},"starfish.agent.RemoteAgent":{consume_asset:[5,1,1,""],create_listing:[5,1,1,""],ddo:[5,1,1,""],download_asset:[5,1,1,""],find_supported_service_type:[5,1,1,""],generate_ddo:[5,1,1,""],get_asset:[5,1,1,""],get_asset_purchase_ids:[5,1,1,""],get_authorization_token:[5,1,1,""],get_endpoint:[5,1,1,""],get_job:[5,1,1,""],get_listing:[5,1,1,""],get_listings:[5,1,1,""],get_metadata_list:[5,1,1,""],invoke:[5,1,1,""],is_access_granted_for_asset:[5,1,1,""],is_did_valid:[5,1,1,""],job_wait_for_completion:[5,1,1,""],load:[5,1,1,""],purchase_asset:[5,1,1,""],purchase_wait_for_completion:[5,1,1,""],register:[5,1,1,""],register_asset:[5,1,1,""],resolve_url:[5,1,1,""],search_listings:[5,1,1,""],service_types:[5,2,1,""],update_listing:[5,1,1,""],upload_asset:[5,1,1,""],validate_asset:[5,1,1,""]},"starfish.asset":{AssetBase:[7,0,1,""],BundleAsset:[8,0,1,""],DataAsset:[9,0,1,""],OperationAsset:[11,0,1,""],create_asset_from_metadata_text:[10,4,1,""],is_asset_hash_valid:[10,4,1,""]},"starfish.asset.AssetBase":{asset_id:[7,1,1,""],did:[7,1,1,""],generateMetadata:[7,1,1,""],get_asset_type:[7,1,1,""],is_asset_type:[7,1,1,""],is_bundle:[7,1,1,""],metadata:[7,1,1,""],metadata_text:[7,1,1,""],name:[7,1,1,""],set_did:[7,1,1,""],type_name:[7,1,1,""]},"starfish.asset.BundleAsset":{add:[8,1,1,""],asset_count:[8,1,1,""],asset_items:[8,1,1,""],asset_names:[8,1,1,""],asset_remove:[8,1,1,""],create:[8,1,1,""],get_asset:[8,1,1,""],get_asset_at_index:[8,1,1,""],is_bundle:[8,1,1,""]},"starfish.asset.DataAsset":{create:[9,1,1,""],create_from_file:[9,1,1,""],data:[9,1,1,""],save_to_file:[9,1,1,""]},"starfish.asset.OperationAsset":{create:[11,1,1,""],is_mode:[11,1,1,""]},"starfish.job":{Job:[14,0,1,""],JobBase:[15,0,1,""]},"starfish.job.JobBase":{IsWorkingStatusList:[15,2,1,""],is_finished:[15,1,1,""],job_id:[15,1,1,""],outputs:[15,1,1,""],status:[15,1,1,""]},"starfish.listing":{Listing:[17,0,1,""],ListingBase:[18,0,1,""]},"starfish.listing.Listing":{get_purchase_ids:[17,1,1,""],is_published:[17,1,1,""],is_purchased:[17,1,1,""],purchase:[17,1,1,""],set_published:[17,1,1,""]},"starfish.listing.ListingBase":{agent:[18,1,1,""],asset_did:[18,1,1,""],data:[18,1,1,""],ddo:[18,1,1,""],did:[18,1,1,""],is_empty:[18,1,1,""],listing_id:[18,1,1,""],purchase:[18,1,1,""]},"starfish.purchase":{Purchase:[21,0,1,""],PurchaseBase:[22,0,1,""]},"starfish.purchase.Purchase":{consume_asset:[21,1,1,""],get_type:[21,1,1,""],is_completed:[21,1,1,""],is_purchase_valid:[21,1,1,""],is_purchased:[21,1,1,""],wait_for_completion:[21,1,1,""]},"starfish.purchase.PurchaseBase":{account:[22,1,1,""],agent:[22,1,1,""],is_purchase_valid:[22,1,1,""],is_purchased:[22,1,1,""],listing:[22,1,1,""],purchase_id:[22,1,1,""]},starfish:{DNetwork:[12,0,1,""],asset:[10,3,0,"-"],provenance:[19,3,0,"-"]}},objnames:{"0":["py","class","Python class"],"1":["py","method","Python method"],"2":["py","attribute","Python attribute"],"3":["py","module","Python module"],"4":["py","function","Python function"]},objtypes:{"0":"py:class","1":"py:method","2":"py:attribute","3":"py:module","4":"py:function"},terms:{"0x00bd138abd70e2f00903268f3db08f2d25677c9":1,"0x3bd774d7d7ee5239c26b39b44b659a2488cc3fcdd17140274b04bfc0a05520f5":25,"3bd774d7d7ee5239c26b39b44b659a2488cc3fcdd17140274b04bfc0a05520f5":25,"45fd1d44764047808b313bf777d98d6304fdf9ff3ba7463aa4346e888ff5041c":25,"abstract":[18,22],"boolean":[1,4,5,7,8,10,11,17,18,21,22],"byte":9,"case":25,"class":[10,24,25],"default":[4,5,11,21],"export":1,"function":1,"import":[1,25],"int":[4,5,8,15],"new":[1,4,5,7,8,9,10,11,24],"public":25,"return":[0,1,4,5,7,8,9,10,11,15,17,18,21,22,25],"static":[1,5,7,8,9,12],"true":[1,4,5,7,8,9,10,11,12,17,18,21,22,25],"try":21,But:0,For:[4,5,23],The:[0,4,5,7,23,25],Then:23,There:0,These:24,With:25,__init__:7,__main__:25,__name__:25,a3392ea6f7b7301bb81c4fe58ad0959360d53662ce3a3d35589f9fbd0e276699:25,abc:[5,7,15,18,22],abi:23,about:[17,18,25],accept:15,access:[4,5,21,23],account:[4,5,12,17,18,21,22,24,26],account_address:12,activ:23,actual:[4,5,25],add:[1,8,9,11],address:[1,5,23,25],against:10,agent:[15,17,18,21,22,24,26],agent_bas:[4,5],agent_url:25,agent_url_did:12,agentbas:[4,5],agentmanag:25,agreement:5,aladdin:25,all:[0,4,5,23,25],allow:[0,4,5,25,26],almost:0,alreadi:[17,21,25],also:[10,24,25],alwai:[4,5],amount:12,ani:[0,8,23,25],aquariu:23,artifact:24,artifacts_path:12,as_checksum_address:1,as_dict:5,ass:[4,5],asset:[0,4,5,17,18,21,22,24,26],asset_agent_did_url:5,asset_bas:[8,9,11],asset_count:8,asset_did:[4,5,17,18],asset_did_id:5,asset_id:[0,5,7,10,12,25],asset_item:8,asset_nam:8,asset_remov:8,asset_typ:7,assetbas:[4,5,7,8,9,11],assign:[4,5,8,9,10,11,15,17,18,25],assum:[4,5,25],auth:5,authent:[5,12,25],author:25,automat:5,avail:[8,23],back:[4,5],barg:[24,25],base:[1,2,4,5,6,8,9,10,11,12,13,14,16,17,20,21,24,25],base_url:5,base_url_or_servic:5,bash:23,basic:25,been:[1,4,5,21,25],befor:[21,25],being:[4,5],below:[4,5,23],between:5,bin:[23,25],block:25,bool:9,both:1,brizo:23,bui:21,bundl:[6,7,24],bundleasset:8,call:[1,5,12,21,25],can:[1,4,5,7,8,9,11,17,21,23,25],cc0:25,central:25,chain:[5,25],charset:25,check:[4,5,10,11,18,21,25],checkout:23,checksum:1,clone:23,collect:8,com:23,combin:0,command:23,compani:23,compar:1,compat:5,complet:[4,5,21,23],configur:25,connect:[0,25],consum:[4,5,21],consume_asset:[4,5,21],contain:[0,1,5,7,8,23,25],content:9,contenttyp:25,contract:[12,21,23,25],contract_nam:12,convert:1,copi:[7,24],core:17,correct:[7,10,21,23],count:[4,5,8],creat:[1,4,5,8,9,10,11,15,17,18,21,23,24],create_asset_from_metadata_text:10,create_from_fil:9,create_list:[4,5,25],current:[5,21],dashboard:23,data:[0,1,4,5,6,11,17,18,21,24,25],dataasset:[4,5,9,25],dataset:25,ddo:[4,5,17,18,25],ddo_text:12,decor:5,def:25,definit:23,dep:[5,25],deploi:23,descript:5,detail:[1,4,5,17,18],develop:12,dex:[23,25],dict:[1,4,5,7,8,9,11,15,17,18],dictionari:[8,9,11],did:[0,4,5,7,8,9,10,11,12,17,18,25],directli:[5,23],dnetwork:24,doc:24,docker:23,doe:[0,5],doing:[22,23],domain:25,download:[0,4,5,21,23,25],download_asset:5,download_path:[5,21],dure:[4,5],earlier:25,els:[1,5,18,21],empti:[8,18],encrypt:1,endpoint:5,enrivorn:23,enter:23,env:25,environ:23,equal:[1,7],error:21,event:21,exampl:[4,5,23,24],execut:5,export_kei:1,export_key_valu:1,extern:[0,23],extra:25,fail:[21,25],failur:[4,5],fals:[1,5,17,18,21],file:[1,9,21,23],filenam:[1,9],find:25,find_network_name_from_id:12,find_supported_service_typ:5,finish:[5,21],first:[0,23,25],folder:23,follow:[1,4,5,23],foobar:25,format:[1,5],found:[4,5,8],from:[1,4,5,8,21,23,25],from_account_address:12,full:24,functional:0,gener:[5,11],generate_ddo:[5,25],generatemetadata:7,get:[5,24,25],get_account:1,get_asset:[5,8],get_asset_at_index:8,get_asset_purchase_id:[4,5],get_asset_typ:7,get_authorization_token:5,get_contract:12,get_endpoint:5,get_ether_bal:12,get_job:5,get_list:[4,5],get_metadata_list:5,get_provenace_event_list:12,get_purchase_id:17,get_token_bal:12,get_typ:21,git:23,github:23,give:[4,5],given:[4,8],givien:[4,5],going:25,hand:[21,25],happen:25,has:[1,4,5,7,17,18,21,25],hash:10,hash_hex:10,have:[4,5,7,21,23,25],held:[1,7,8,18],help:25,here:[4,5,25],hex:10,hold:8,how:25,http:[5,23,25],ids:[4,5],imag:23,immut:7,import_kei:1,import_key_valu:1,index:8,info:5,inforamiton:[4,5],inform:[1,17,18,25],input:5,instal:[12,24],instanc:24,instead:25,integ:21,interact:[0,23],interegr:23,intergr:23,internal:25,invalid:21,invok:[5,11],is_access_granted_for_asset:[4,5],is_add_proof:5,is_address_equ:1,is_asset_hash_valid:10,is_asset_typ:7,is_async:5,is_bundl:[7,8],is_complet:21,is_did_valid:5,is_empti:18,is_finish:15,is_mod:11,is_password:1,is_publish:17,is_purchas:[17,21,22],is_purchase_valid:[21,22],is_read:9,is_token_s:12,is_valid:1,issu:[4,5],isworkingstatuslist:15,item:[0,5],job:[5,24],job_bas:14,job_id:[5,14,15],job_wait_for_complet:5,jobbas:[14,15],json:1,json_text:1,just:25,keeper:24,kei:1,key_fil:1,key_valu:1,keyfil:1,koi:[5,23],latest:23,left:5,let:25,librari:[24,25],licens:25,like:23,link:25,list:[4,5,15,21,22,24,25],listing_bas:17,listing_data:[4,5,25],listing_id:[4,5,17,18,25],listingbas:[17,18],listinng:18,load:[1,5,25],load_development_contract:[12,25],load_from_fil:1,local:[12,24,25],localhost:[5,25],log:25,made:[4,5],main:25,make:[4,5,7,23],manag:[9,25],mani:8,market:[4,5],maximum:[4,5],mayb:7,meaningful:21,memori:[0,2,24,25],memoryag:[0,4],messag:21,meta:5,metadata:[0,4,5,7,8,9,10,11,25],metadata_text:[7,8,9,10,11],method:[1,4,5,7,21,25],mode:11,mode_typ:11,modul:[6,24],more:[21,25],mutabl:7,my_result:[4,5],myasset:25,myproject:23,name:[1,5,7,8,9,11,12,25],need:[1,12,23,25],network:[0,1,4,5,9,12,23,25,26],network_id:12,next:25,node:[12,24],non:11,none:[1,4,5,7,8,9,10,11,12,14,15,17,18,25],notic:25,now:[23,25],number:[4,5,8],object:[1,4,5,7,8,10,12,15,17,18,21,22,25],obtain:25,ocean:[1,4,5,9,24,25],oceanpurchaseerror:21,oction:7,off:5,offset:[4,5],onc:[10,23],one:1,onli:[5,12,25],opensesam:25,oper:[5,6,24,26],operationasset:[5,11],option:[5,8,9,10,11,17,18,21,25],other:0,ouptut:15,our:25,out:[5,25],output:[14,15],overal:24,page:[4,5],paper:25,param:[1,5,17],paramat:[4,5],paramet:[1,4,5,7,8,9,10,11,15,17,18,21],pass:[4,5],password:[1,5,12,25],path:[5,21],payment:[4,5],perform:11,place:[4,5],plain:25,point:[4,5],poll:5,price:[5,25],print:[5,25],privat:1,probabl:25,process:[4,5],project:23,properti:[1,5,7,8,9,12,15,17,18,21,22,25],protocol:[23,25],proven:24,provid:[0,4,5,8,9,11,25],publish:17,purcas:[17,18],purchas:[4,5,17,18,24],purchase_asset:[4,5],purchase_bas:21,purchase_id:[4,5,17,18,21,22],purchase_wait_for_complet:[4,5],purchasebas:[21,22],python3:25,python:23,rais:[8,21],raw:1,raw_kei:1,read:[5,9],readi:12,receiv:21,record:[4,5,25],refer:24,reference_1:12,reference_2:12,regis:25,regist:[0,4,5,8,9,11,24],register_account:5,register_asset:[4,5,25],register_did:12,register_provenac:12,registr:[4,5,25],regsit:5,rememeb:25,remot:[2,24],remoteag:[5,25],remov:8,renam:21,repo:23,repositori:23,request_ether_from_faucet:12,request_test_token:12,requir:[21,23],resolv:[5,25],resolve_ag:12,resolve_did:12,resolve_url:5,result:[4,5,15,17],root:23,run:[15,24,25],sale:5,same:[0,1,5,7,10,21,25],sampl:[5,25],save:[1,9,24],save_key_fil:1,save_to_fil:[1,9],schedul:15,script:23,search:[4,5],search_list:[4,5],search_name_typ:5,search_registered_asset:[4,5],second:[0,5,21,25],secret:[1,23],see:[4,5,11,18,21,24,25],sell:25,send:5,send_eth:12,send_token:12,send_token_and_log:12,separ:23,server:[4,5,25],servic:[0,5,11,25],service_agreement_id:[17,18],service_list:5,service_typ:5,session:23,set:[1,7,17,18],set_did:7,set_password:1,set_publish:17,setup:24,should:23,show:25,sign_transact:1,sinc:25,sleep:5,sleep_second:5,sleep_time_second:12,smart:21,solut:7,some:[5,21,25],someth:23,sort:[4,5],sourc:23,specifi:25,spree:23,squid:21,squidag:18,squidpurchas:[17,18],stack:23,starfish:[1,4,5,7,8,9,10,11,12,14,15,17,18,21,22,23,25],start:[24,25],start_ocean:23,startup:24,statu:[5,14,15],storag:5,store:[1,5,7,23,25],str:[1,4,5,7,8,9,10,11,15,17,18,21,22],string:[1,5,8,9,10,21],sub:[7,8],subclass:5,successful:21,suit:23,support:[5,11,25],surfer:[0,5,23,25],surfer_did:0,surferag:[0,5],syntax:5,tag:23,task:25,templat:[4,5],termin:23,test:[5,10,17,21,24,25],testasset:25,text:[1,4,5,7,10,25],them:23,thi:[0,1,4,5,7,8,9,11,12,15,17,18,21,22,23,25],three:0,time:[5,25],timeout:5,timeout_second:[5,12,21],timeoutsecond:[4,5],to_account_address:12,todo:[4,5],token:5,too:[1,21],tool:24,transact:1,trust:5,two:[1,23,25],type:[0,1,4,5,7,8,9,10,11,15,17,18,21,22,25],type_nam:7,underl:17,underli:[17,18,21],uning:21,unit:24,until:23,updat:[4,5],update_list:[4,5],upload:[0,24],upload_asset:[5,25],uri:5,url:[5,12,25],usag:5,use:[4,5,17,18,23,25],used:[1,4,5,8,9,11,21],usernam:[5,12,25],using:[0,4,5,9,17,18,23,25],usr:25,utf:25,valid:[4,5,9,21,22],validate_asset:[4,5],valu:[1,4,5,17,21],valueerror:8,venv:23,version:23,view:25,virtual:5,virtualvenv:23,waif:21,wait:[4,5,12,21,23],wait_for_complet:21,wait_for_migration_and_extract_keeper_artifact:23,want:25,weather:[4,5],web3:[1,12],what:25,where:[0,12,25],white:25,within:[7,8,17,18],without:23,work:[0,23,25],write:1,writer:25,written:25,xxxx:1,xxxxx:5,yet:[4,5],you:[0,1,21,23,25,26],yyyi:[1,5]},titles:["Starfish Agents","Account class","Agent Classes","Agent Base class","Memory Agent class","Remote Agent class","Asset Classes","Asset Base class","Bundle Asset class","Data Asset class","Asset Module","Operation Asset class","DNetwork class","Job Classes","Job class","Job Base class","Listing Classes","Listing class","Listing Base class","Provenance module","Purchase Classes","Purchase class","Purchase Base class","Getting Started","starfish-py API Documentation","Register asset on a remote agent","Starfish Tools"],titleterms:{"class":[1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,20,21,22],"new":25,account:1,agent:[0,2,3,4,5,25],api:24,artifact:23,asset:[6,7,8,9,10,11,25],barg:23,base:[3,7,15,18,22],bundl:8,content:24,copi:23,creat:25,data:9,dnetwork:[12,25],document:24,exampl:25,full:[23,25],get:23,instal:23,instanc:25,job:[13,14,15],keeper:23,librari:23,list:[16,17,18],local:23,memori:4,modul:[10,19],node:23,ocean:23,oper:11,proven:19,purchas:[20,21,22],regist:25,remot:[5,25],run:23,save:25,setup:25,starfish:[0,24,26],start:23,startup:23,test:23,tool:26,unit:23,upload:25}})