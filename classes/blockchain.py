import hashlib as hl
from functools import reduce
import random
import json
import pickle
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Validation


class Blockchain:
    def __init__(self, hosting_node_id):
        GENESIS_BLOCK = Block(0, "_", [], 123, 0)
        self.chain = [GENESIS_BLOCK]
        self.__open_transactions = list()
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val
        # pass instead of setting self.__chain would make chain immutable

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain_db.txt', mode='r') as f:
                # rb is for pickle to (r)ead (b)inary, change back to mode='r' (read) for json
                file_content = f.readlines()
            # file_content = pickle.loads(f.read())
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            # ALL CODE BELOW IS FOR USE FOR CONVERTING BACK AND FORTH IN JSON

            #
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = list()
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount'])
                                for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'],
                                      converted_tx, block['proof'], block['timestamp'])

                load_participants = (part['sender']
                                     for part in block['transactions'])
                # participants.add(load_participants)

                updated_blockchain.append(updated_block)
            self.chain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = list()
            for tx in open_transactions:
                updated_tx = Transaction(
                    tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_tx)
            self.__open_transactions = updated_transactions
            # return load_participants
        except (IOError, IndexError):
            pass
        finally:
            print("Clean up!!")

    def save_data(self):
        try:
            with open('blockchain_db.txt', mode='w') as f:
                # Change mode to 'mode=wb' to use to use pickle
                chain_dicts = [block.__dict__ for block in [Block(ele.index, ele.previous_hash, [
                    tx.__dict__ for tx in ele.transactions], ele.proof, ele.timestamp) for ele in self.__chain]]
                f.write(json.dumps(chain_dicts))
                f.write('\n')
                savable_tx = [
                    trans.__dict__ for trans in self.__open_transactions]
                f.write(json.dumps(savable_tx))
            # save_data = dict({
            #     'chain': blockchain,
            #     'ot': open_transactions
            # })
            # f.write(pickle.dumps(save_data))
        except (IOError, IndexError):
            print("Saving failed!")

    def more_than_1_block(self):
        longer_than_1 = False
        if len(self.__chain) > 1:
            longer_than_1 = True
        return longer_than_1

    def get_last_blockchain_value(self):
        if more_than_1_block():
            return None
        return self.__chain[-1]

    def get_balance(self):
        participant = self.hosting_node
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant]for block in self.__chain]
        tx_sender.append(open_tx_sender)

        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if tx_amt else tx_sum + 0, tx_sender, 0)

        open_tx_recipient = [tx.amount
                             for tx in self.__open_transactions if tx.recipient == participant]
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        tx_recipient.append(open_tx_recipient)

        amount_recieved = reduce(
            # This ternary adds the sum a transaction about on a block to the 'tx_sum' var
            # if the tx_amount list has values. If there is no tx_amt 0 is added to sum
            # (a pass basically)
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if tx_amt else tx_sum + 0, tx_recipient, 0)

        return round((amount_recieved - amount_sent), 2)

    def add_value(self, recipient, sender, amount=1.0):
        """
        Appends a new value as well as the last block
        to the blockchain
        Arguments:
        :sender: The sender of the coins [String]
        :recipient: The recipient of the coins [String]
        :amount: The amount of coins sent in the transaction (default = 1.0)
        """
        transaction = Transaction(sender, recipient, amount)

        if Validation.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(str(recipient).lower())
            self.save_data()
            return True
        else:
            return False

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Validation.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def mine_block(self):
        """ Creates a new block in the blockchain adding current open transactions to it."""
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        copied_transactions = self.__open_transactions[:]
        reward = Transaction('MINING', self.hosting_node, 10)
        copied_transactions.append(reward)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = list()
        self.save_data()
        print(
            f"Blockchain: {[block.__dict__ for block in [Block(ele.index,ele.previous_hash,[tx.__dict__ for tx in ele.transactions],ele.proof,ele.timestamp) for ele in self.__chain]]}")
        return True

    def add_transaction(self):
        tx_amount = self.get_transaction_value()
