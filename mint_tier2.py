import sys
from web3 import Web3
import config
from abis import tier2

web3 = Web3(Web3.HTTPProvider(config.RPC))
account = web3.eth.account.from_key(config.private_key)

def buy(quantidade):
    merkleProof = []
    code = 'gg'
    nonce = web3.eth.get_transaction_count(web3.to_checksum_address(account.address))
    payment_amount = web3.to_wei(tier2.price * quantidade, 'ether')
    to_address = web3.to_checksum_address(tier2.contract_address)
    contract = web3.eth.contract(address=to_address, abi=tier2.abi)
    data = contract.encodeABI(fn_name='whitelistedPurchaseWithCode', args=[payment_amount, merkleProof, payment_amount, code])

    while True:
        try:
            transaction = {
                'from': account.address,
                'to': to_address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': web3.to_wei('2', 'gwei'),
                'data': data
            }

            signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f'transaction: {tx_hash.hex()}')
            nonce += 1
        except Exception as e:
            if e != 'execution reverted: sale has not begun':
                print(e)
                break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        buy(quantidade=int(sys.argv[1]))
    else:
        print("informe a quantidade a ser mintada, Exemplo: python buy.py 5")
