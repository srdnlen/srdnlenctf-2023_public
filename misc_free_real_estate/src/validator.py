import web3
import json
import random
import string
import os

FLAG = os.environ.get("FLAG")
api_key = os.environ.get("ALCHEMY_API_KEY")
TOKEN_LEN=32

contract_abi = """[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "newAd",
				"type": "string"
			}
		],
		"name": "buyAdSpace",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "createAccount",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "int256",
				"name": "tickets",
				"type": "int256"
			}
		],
		"name": "redeem",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "accounts",
		"outputs": [
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "checkAccountStatus",
		"outputs": [
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			},
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "freebies",
		"outputs": [
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "registered",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "showAd",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""


def get_contract_address():
    # TODO: andrebbe istanziato un contratto per richiesta/team. Altrimenti fare un leak del metodo sarebbe facile, anche se in realtà la chall è così facile che non conta molto.
    return "0x6BCdE7Ce8ea0CBD7D894a0772b8e47B5EFF8b391"

def setup_contract_web3():
    abi_json = json.loads(contract_abi)
    w3 = web3.Web3(web3.HTTPProvider(api_key))
    #print(w3.eth.get_block('latest'))
    contract = w3.eth.contract(address=get_contract_address(), abi=abi_json)
    return contract

def check_token(expected,contract):
    current = contract.functions.showAd().call()
    print(f"The current ad seems to be: {current}")
    return expected == current

def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def gen_token():
    return get_random_string(TOKEN_LEN)

def client_loop(contract,token):
    print("Welcome to Free Real Estate, where the rich get richer!")
    print(f"The smart contract is at address {contract.address} on the sepolia testnet")
    print(f"Place the following token in the ad space:")
    print(f"        {token}")
    print("Write I AFFIRM if you did that and we'll check.")
    input(">")
    if check_token(token, contract):
        print(f"Correct! The flag is {FLAG}")
    else:
        print("They don't seem to match. \nIf you did it too early, wait for the block to get confirmed. \nIf you did it too late, maybe another team messed with it. \nJust try again.")

    pass

if __name__ == "__main__":
    contract = setup_contract_web3()    
    token = gen_token()
    client_loop(contract,token)
