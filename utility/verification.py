"""Provides helper methods for Validation and Verification of Blockchain Transactions """

import hashlib as hl
from utility.hash_util import hash_256, hash_block
from transaction import Transaction
from wallet import Wallet


class Validation:

    @staticmethod
    def valid_proof(transaction, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transaction]) + str(last_hash) +
                 str(proof)).encode()
        guess_hash = hash_256(guess)
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_chain(cls, blockchain):
        """Verifies the validiity of the current blockchain"""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('POW is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(trans, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= trans.amount and Wallet.verify_trans_sig(trans)
        return Wallet.verify_trans_sig(trans)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])
