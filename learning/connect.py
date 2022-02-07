import json
import base64
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn

# Function from Algorand Inc. - utility for waiting on a transaction confirmation
def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo

def first_transaction_example(private_key, my_address):
    algod_address="http://localhost:4001"
    algod_token="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000
    receiver = "Q2ZRIBW5J35R45HV25UXYUVK6JB34NJ7EWI5L3KHHXSJDPJWP2MHKCNTCI"
    note = "Hello World".encode()

    tx = PaymentTxn(my_address, params, receiver, 1000000, None, note)
    signed_txn = tx.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)
    ))
    print("Decoded note: {}".format(
        base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()
    ))

    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")



first_transaction_example("UAd+6NtEaGoC3ZqWrkR3JJ9UpqjOCevfxlgh+Vd/Gz+tF94D0COfKeHLiEsAMKulNCG0+Au6jQXGLwDR2MDKfw==", "VUL54A6QEOPSTYOLRBFQAMFLUU2CDNHYBO5I2BOGF4ANDWGAZJ7VQTLF6E")
