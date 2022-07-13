from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node

api_url = f"https://mainnet.infura.io/v3/05d545fd8cc5446a9b6e02369555a845"
web3 = Web3(HTTPProvider(api_url))
assert web3.isConnected(), f"Failed to connect to provider at {url}"

print("Successfully connected to Ethereum node.")

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }
	
	#YOUR CODE HERE	
	
	contract = web3.eth.contract(address=contract_address, abi=abi)
	URI = contract.functions.tokenURI(apeID).call()
	sample_owner = contract.functions.address(1)
	
	
	print(URI)
	cid = "QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/"+str(apeID)
	
	params = (('arg', cid),)
	response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params)

	response_dict = response.json()
	print(response_dict)
	data['image'] = response_dict.get('image')
	attributes = response_dict.get('attributes')
	
	for attribute in attributes:
		if attribute.get('trait_type') == 'Eyes':
			data['eyes'] = attribute.get('value')
			break
	
	print(data)
	print(sample_owner)
	data['owner'] = sample_owner
	
	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

