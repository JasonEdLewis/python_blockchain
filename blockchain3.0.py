import hashlib as hl
from functools import reduce
import random
import json
from collections import OrderedDict
from mining_reward import owner, MINING_REWARD

from hash_util import hash_block
from pow import valid_proof

GENESIS_BLOCK = {
    "index": 0,
    "previous_hash": "_",
    "transactions": [],
    "proof": 123
}
blockchain = [GENESIS_BLOCK]
open_transactions = []

participants = set({owner})


def load_data():
    with open('blockchain_db.txt', mode='r') as f:
        file_content = f.readlines()
        global blockchain, open_transactions
        blockchain = json.loads(file_content[0][:-1])
        open_transactions = json.loads(file_content[1])


load_data()


def save_data():
    with open('blockchain_db.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))


def more_than_1_block():
    longer_than_1 = False
    if len(blockchain) > 1:
        longer_than_1 = True
    return longer_than_1


def get_last_blockchain_value():
    if more_than_1_block():
        return None
    return blockchain[-1]


def add_value(recipient, sender=owner, amount=1.0):
    """
    Appends a new value as well as the last block
    to the blockchain
    Arguments:
    :sender: The sender of the coins [String]
    :recipient: The recipient of the coins [String]
    :amount: The amount of coins sent in the transaction (default = 1.0)
    """
    # transaction = {"sender": sender,
    #                "recipient": recipient,
    #                "amount": amount}
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(str(recipient).lower())
        save_data()
        return True
    else:
        return False


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant]for block in blockchain]
    tx_sender.append(open_tx_sender)

    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if tx_amt else tx_sum + 0, tx_sender, 0)

    open_tx_recipient = [tx['amount']
                         for tx in open_transactions if tx['recipient'] == participant]
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    tx_recipient.append(open_tx_recipient)

    amount_recieved = reduce(
        # This ternary adds the sum a transaction about on a block to the 'tx_sum' var
        # if the tx_amount list has values. If there is no tx_amt 0 is added to sum
        # (a pass basically)
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if tx_amt else tx_sum + 0, tx_recipient, 0)

    return round((amount_recieved - amount_sent), 2)


def verify_transaction(trans):
    sender = trans['sender']
    return get_balance(sender) > trans['amount']


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def mine_block():
    """ Creates a new block in the blockchain adding current open transactions to it."""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    copied_transactions = open_transactions[:]
    copied_transactions.append(MINING_REWARD)

    block = {
        "index": len(blockchain),
        "previous_hash": hashed_block,
        "transactions": copied_transactions,
        "proof": proof
    }
    # print(f"""
    # Hashed Block: {block}

    # """)
    blockchain.append(block)
    print(f"Blockchain: {blockchain}")
    return True


def get_transaction_value():
    """Returns user input for requested transaction

    Args:
    sender(string)
    recipient(string)
    amount(int)

    Returns:
    value(int)
     """
    sender = owner
    owner_balance = get_balance(owner)
    amount = float(input("How many coins would you like to send? "))
    if amount > owner_balance:
        return (False, round(amount, 2))
    recipient = input(f"Whom would you like to send these {amount} coins: ")
    return (recipient, amount)


def add_transaction():
    tx_amount = get_transaction_value()


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    print("_"*20)
    for (index, block) in enumerate(blockchain):
        print(f"Blockchain index {index}:{block}")
    else:
        print("-"*20)


def verify_chain():
    """Verifies the validiity of the current blockchain"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('POW is invalid')
            return False
    return True


waiting_for_input = True
while waiting_for_input:
    print("Please Choose")
    print("1: Add transaction")
    print("2: Output the Blockchain blocks")
    print("q: Quit")
    print("h: Manipulate")
    print("3: Mine Block")
    print("4: Show participants")
    print("5: Verify transactions")
    print("t: show open transactions")

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if not recipient:
            print(f""" *WARNING*
   You dont have enough to sent {amount} coins """)
            continue
        if add_value(recipient, amount=amount):
            print(f"""{'*'*20}
                      Transaction added succesfully
                      {'*'*20}""")
        else:
            print("Failed to add transation")

        # print(open_transactions)
    elif user_choice == '2' and len(blockchain) > 0:
        print_blockchain_elements()
        continue
    elif user_choice == 'q':
        waiting_for_input = False
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                "index": 0,
                "previous_hash": "_",
                "transactions": [{"sender": "todd", "recipient": "Jason", "Amount": 101}]
            }
    elif user_choice == '3':
        if mine_block():
            open_transactions = []
            save_data()
        # print(f"Open transaction post mining: {open_transactions}")
    elif user_choice == 't':
        print(open_transactions)
    elif user_choice == '4':
        print(f"""
        Wallet owners: {participants}
        """)
    elif user_choice == '5':
        if verify_transactions():
            print("All transactions valid")
        else:
            print("There are invalid transactions")
    else:
        print("Please enter a valid value")

    if not verify_chain():
        print_blockchain_elements()
        print("Invalid Blockchain!")
        break
    print(f"{owner}'s Balance: {get_balance(owner)}")

print("Done!")
