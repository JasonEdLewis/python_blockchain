import hashlib as hl
from hash_util import hash_256



def valid_proof(transaction, last_hash, proof):
    guess = (str(transaction) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_256(guess)
    # print(guess_hash)
    return guess_hash[0:2] == "00"
