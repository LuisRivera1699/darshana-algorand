import json
import base64
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn, AssetConfigTxn

import requests
import json

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

def create_project_asset(private_key, my_address, metadata_path, p_id):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000
    receiver = "Q2ZRIBW5J35R45HV25UXYUVK6JB34NJ7EWI5L3KHHXSJDPJWP2MHKCNTCI"
    note = "Project finished".encode()

    txn = AssetConfigTxn(
        sender=my_address,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name="DARSHP",
        asset_name="PID{}".format(p_id),
        manager=my_address,
        reserve=my_address,
        freeze=my_address,
        clawback=my_address,
        url=metadata_path,
        decimals=0)

    # Sign with secret key of creator
    stxn = txn.sign(private_key)

    # Send the transaction to hte network and retrieve the txid
    txid = algod_client.send_transaction(stxn)
    print(txid)

    wait_for_confirmation(algod_client, txid)

    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print("Created asset: {}".format(asset_id))
    except Exception as e:
        print(e)



print("Darshana job certification rough flow:\n")
print("Starting the app:\n\n\n\n")

print("Simulating recruiter creates a project:\n")

value = input("Hello recruiter, how many projects you'd like to create:")

projectList = []

print("\nCreating projects... \n")

for i in range(0, int(value)):
    print("\nCreating project number {}\n\n".format(i+1))
    name = input("Set the name for your project: ")
    description = input("Set the description for your project: ")
    price = input("How many are you going to pay for this project in USD: ")
    projectList.append(
        {   
            'id': i,
            'name': name,
            'description': description,
            'price': price
        }
    )

print("Finished creating projects. Switching to Talent... \n")
print("Simulating talents apply for a project:\n")

print("Hello tallent, here are the created projects:\n")

for i in range(0, len(projectList)):
    print('Project ID Nº{}'.format(i))
    print('Project name: {}'.format(projectList[i]['name']))
    print('Project description: {}'.format(projectList[i]['description']))
    print('Project payment: {}'.format(projectList[i]['price']))
    print('\n')

pid = input("Which project are you going to apply, enter the id:")

print("Successfully applied to: Project ID {}\n\n".format(pid))

project = projectList[int(pid)]

print("Simulating recruiter accepts/deny an application:\n")

print("Hey recruiter, you have an application for Project ID {}".format(pid))

accept = input('Would you like to accept it?: 0 NO | 1 YES:')

if (accept == '1' or accept == 'YES'):
    print("\nSimulating talent complete a project:\n")
    print("Hey talent, you've been accepted for Project ID {}\n".format(pid))

    input("Press enter when you finish the project to make a submission:")

    print("\nSimulating recruiter accept the project submission:\n")

    print("Hey recruiter, the talent has submitted to finish the project:")

    finish = input('Would you like to accept it?: 0 NO | 1 YES:')

    if (finish == '1' or finish == 'YES'):
        print("\nUploading project metadata to IPFS and printing it:\n")
        response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files={'project': str(projectList[int(pid)])})
        p = response.json()
        print(p['Hash'])
        path = "https://ipfs.infura.io/ipfs/{}".format(p['Hash'])
        create_project_asset("UAd+6NtEaGoC3ZqWrkR3JJ9UpqjOCevfxlgh+Vd/Gz+tF94D0COfKeHLiEsAMKulNCG0+Au6jQXGLwDR2MDKfw==", "VUL54A6QEOPSTYOLRBFQAMFLUU2CDNHYBO5I2BOGF4ANDWGAZJ7VQTLF6E", path, pid)
    else:
        print("Program finished because of recruiter didn't accept the finish submission.")
else:
    print("Program finished because of recruiter didn't accept the application.")
