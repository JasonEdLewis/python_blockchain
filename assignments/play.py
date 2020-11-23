import functools
import random as ran
import hashlib as hl
from collections import OrderedDict


the_crew = OrderedDict([('sender', 'MINER'), ('recipient', 'Jason'), (
    'amount', 10), ('sender', 'Jason'), ('recipient', 'jube'), ('amount', 4.2)])

# new_dict = {thing[key], thing[val] for thing in the_crew}

# print(new_dict)


def valid_proof(transaction, last_hash, proof):
    guess = (str(transaction) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess)
    print(guess_hash.hexdigest())


# valid_proof({'sender': 'MINER', 'recipient': 'Jason', 'amount': 10},
#             'c70e5e087c4af6b0c16ede032d443dde180c46205ac242fb10a74e12ac1c180e', 9)
# the_num = ran.randint(0, 77)


# print(the_num)
# Transactions_sent = [[], [], []]

# x_tx = [thing for thing in Transactions_sent if thing]

# Received_transactions = [[], [10], []]
# x_rec = [thing for thing in Received_transactions if thing]

# num_list = [[], [2], [], [10], [], [], [19]]


# sum_list = functools.reduce(
#     lambda the_sum, the_next: the_sum + the_next[0] if len(the_next) > 0 else the_sum, num_list, 0)

# print(sum_list)
# summed_txs = functools.reduce(
#     lambda tx_sum, tx_amt: tx_sum + tx_amt[0], Received_transactions, 0)

# print(x_rec[0])

# trans = [{'sender': 'Jason', 'recipient': 'Greg', 'amount': '9.24'},
#          {'sender': 'Jason', 'recipient': 'courtney', 'amount': '5.21'},
#          {'sender': 'Jason', 'recipient': 'Pete', 'amount': '5.21'}
#          ]

# owners = {'trish', 'courtney', 'Jason', 'Greg'}

# balances = []


# def update_balances():
#     tran = trans[-1]
#     if tran:
#         for wal in balances:
#             if wal['name'] in owners:
#                 wal['name']['balance'] += tran['amount']
#                 print(balances)
#     else:
#         for t in trans:
#             if t['recipient'] not in owners:
#                 balances.append(
#                     {'name': t['recipient'], 'balance': t['amount']})


# update_balances()
# print('Balances: ', balances)
