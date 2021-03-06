import json
import hashlib as hl
# __all__ = ['hash_256', 'hash_block']


def hash_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [
        tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_256(json.dumps(hashable_block, sort_keys=True).encode())
