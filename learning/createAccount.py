from algosdk import account, encoding

# generate an account
private_key, address = account.generate_account()
print("Private key:", private_key)
print("Address:", address)

# Check if the address is valid
if encoding.is_valid_address(address):
    print("the address is valid")
else:
    print("the addres is invalid.")