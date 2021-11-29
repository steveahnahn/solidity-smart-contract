import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

from solcx import compile_standard, install_solc

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.6.0")

# compile our solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode - walking down the json of our compiled metadata
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]


# connecting to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/187eee434ec54921a5c490e6d8c79ab7")
)
chain_id = 4
my_address = "0xf285Af0889FBDC953A136df9c62463eEEF35A229"
# always add 0x in front of private key
private_key = os.getenv("PRIVATE_KEY")


# # Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction count
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)


# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")

# Working with hte contract, you always need
# Contract Address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value (view)
# Transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

transaction_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
print("Updating Contract information...")
store_tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print("Contract state changed")

print(simple_storage.functions.retrieve().call())
