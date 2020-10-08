MINING_REWARD = 10

GENESIS_BLOCK = {
    'previous_hash': ' ',
    'transactions': [],
    'index': 0,
}

blockchain = [GENESIS_BLOCK]
open_transactions = []
balances = []
# balances = [{'name': 'Jason', 'balance': 100}]
owner = "Jason"
participants = {"jason"}


def hash_block(block):
    return ''.join([str(block[key]) for key in block])


def blockchain_not_empty():
    something = False
    if len(blockchain) >= 1:
        something = True
    return something


def view_blockchain():
    print('blockchain: ', blockchain)


def show_parcipitants():
    print(participants)


def add_transaction(recipient, sender=owner, amount=1.0):
    """
    Appends a new transtion to the blockchain which includes the:
    :sender: The sender of the coins.
    :recipient: The receiver of the coins.
    :amount: amount of coins sent.
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    # participants.add(sender)
    if not verify_trans(transaction):
        participants.add(recipient)
        open_transactions.append(transaction)
        update_balances()
        print('Open transactions: ', open_transactions)
    # else:
    #     print(
    #         f"You dont have enough to send this amount. Please send {transaction['amount']} or less.")


def get_transaction():
    amount = float(input("How many JCoins would you like to send? "))
    # if amount == ValueError.args():
    #     print('Please enter a numerical amount')
    #     get_transaction()
    recipient_name = input(f"who are you sending {amount} Jcoins to? ")
    return (recipient_name, amount)
    # I could just execute the function * add_transaction(recipient_name, amount) *
    #  right here but I will practice the tuple in the return statement above


# def clear_transactions():
#     global open_transactions
#     open_transactions = []

    # MINE BLOCK


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # print(hashed_block)
    reward_trans = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    open_transactions.append(reward_trans)
    block = {
        'previous_hash': hashed_block,
        'transactions': open_transactions,
        'index': len(blockchain),
    }
    blockchain.append(block)
    update_balances()
    return True
    # open_transactions.clear()
    # clear_transactions()


def verify_trans(trans):
    print("Verify Trans sender: ", trans['sender'])
    sender_balance = get_balance(trans['sender'])
    print(f"Verified sender balance:  {sender_balance}")
    return sender_balance >= trans['amount']


def validate_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def bc_elements():
    for block in blockchain:
        print(block)


def show_open_transactions():
    print(open_transactions)


def update_balances():
    if len(open_transactions) == 0:
        return
    else:
        tran = open_transactions[-1]
        # print("Trans: ", tran, "balances: ", balances)
        sender = tran['sender'].lower()
        recipient = tran['recipient'].lower()
        amount = float(tran['amount'])
        # print("in participants: ", sender, " ", recipient, " ", amount)
        if len(balances) != 0:
            for u in balances:
                if u['name'] == recipient:
                    u['balance'] += amount
                elif u['name'] == sender:
                    u['balance'] -= amount
        else:
            balances.append({"name": recipient, "balance": amount})
            participants.add(sender)
            participants.add(recipient)
    all_balances()
    return balances
    # name = user['name'].lower()
    # balance = float(user['balance'])
    # print("name: ", name, "balance: ", balance)
    # if name == sender and name != "MINING":
    #     print("sender: ", balance - amount)
    #     user['balance'] = balance - amount
    # if recipient in participants:
    #     if name == recipient:
    #         print("recipient: ", balance + amount)
    #         user['balance'] = balance + amount
    # else:
    #     participants.add(recipient)
    #     balances.append({'name': recipient, 'balance': amount})
    #     all_balances()
    # break
# Use the function below to expand the ability to get the balances of other participants when blockchain expands to other nodes


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    senders_open_txs = [[tx['sender'] for tx in trans['amount']
                         if tx['sender'] == participant] for trans in open_transactions]
    print("get balance tx sender: ", senders_open_txs)
    tx_sender.append(senders_open_txs)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recieved = [[tx['amount'] for tx in block['transactions']
                    if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recieved:
        if len(tx) > 0:
            amount_received += tx[0]
    update_balances()
    return amount_received - amount_sent


def user_choice():
    user_data = input("Choose: ")
    return user_data


def all_balances():
    print(balances)


def check_balance():
    name = input("Whose balance would you like to check? ").lower()
    if name not in participants:
        print("That wallet owner doesnt exist")
        return
    else:
        return get_balance(name)


def validate_transactions():
    return all([verify_trans(tx) for tx in open_transactions])


keep_going = True

while keep_going:
    """
    Will run forever because there is nothing changing this to 'False'
    """
    print("""
    1: Add a new transaction
    2: Output the blocks
    3: Manipulate
    4: Mine block
    5: Open Transactions
    6: Check Transaction Validity
    7: BlockChain
    8: Wallet Owners
    9: Balances
    q: Quit
     """)
    the_choice = user_choice()
    if the_choice == '1':
        tx_data = get_transaction()
        # destructoring of tx_data - from imputs - setting amount and recipient to corresponding tx_data values. Can only be done with tuple
        recipient, amount = tx_data
        add_transaction(recipient=recipient, amount=amount)

    elif the_choice == '2':
        if blockchain_not_empty():
            bc_elements()
        else:
            print("There are no blocks to show")
            continue
    elif the_choice == '3':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'transactions': [{'sender': 'Kent', 'recipient': 'Jason', 'amount': 124.98}],
                'index': 0,
            }
    elif the_choice == '4':
        mine_block()
    elif the_choice == '5':
        show_open_transactions()
    elif the_choice == '6':
        if validate_transactions():
            print("all transactions are valid")
        else:
            print("There are some invalid transactions")
    elif the_choice == '7':
        view_blockchain()
    elif the_choice == '8':
        show_parcipitants()
    elif the_choice == '9':
        all_balances()
    elif the_choice == 'q':
        keep_going = False
    else:
        print("Invalid choice. Please choice 1 - 4")
    if not validate_chain():
        # print(f'Validate chain value: {validate_chain()}')
        bc_elements()
        print("__"*30)
        print("Invalid Blockchain!")
        break
    # print(f"Your current balance is: {get_balance('Jason')}")
    print("Participants: ", participants)
