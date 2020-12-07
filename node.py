from flask import Flask, jsonify, request, send_from_directory
from wallet import Wallet
from flask_cors import CORS
from blockchain import Blockchain
from utility.common import std_response
import json


app = Flask(__name__)
wallet = Wallet()
blockhain = Blockchain(wallet.public_key)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    keys_saved = wallet.save_keys()
    if keys_saved:
        global blockhain
        blockhain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': blockhain.get_balance()
        }
        return jsonify(response), 201
    return std_response('Saving keys failed', keys_saved), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    wallet_loaded = wallet.load_keys()
    if wallet_loaded:
        global blockhain
        blockhain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': blockhain.get_balance()
        }
        return jsonify(response), 200
    return std_response('Loading keys failed', False), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockhain.get_balance()
    if balance != None:
        return jsonify({'message': 'Funds retrieved successfully.', 'balance': balance}), 200
    return std_response('failed to load balance', False), 500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        return std_response("No wallet set up to send from", False), 400
    values = request.get_json()
    if not values:
        return std_response('No values sent', False), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        return std_response('recipient or amount missing', False)
    recipient = values['recipient']
    amount = values['amount']
    sig = wallet.sign_transaction(
        wallet.public_key, recipient, amount)
    new_block = blockhain.add_value(
        recipient, wallet.public_key, sig, amount)
    if new_block:
        response = {"message": f"You succesfully sent {amount} jcoins to {recipient}", "balance": blockhain.get_balance(),
                    "transaction": {
            "sender": wallet.public_key,
            "recipient": recipient,
            "amount": amount,
            "signature": sig
        }
        }
        return jsonify(response), 201
    response = {
        "message": "Tranastion failed",
        "balance": blockhain.get_balance()
    }
    return jsonify(response), 400


@app.route('/transactions', methods=['GET'])
def get_transactions():
    open_txs = blockhain.get_open_transactions()
    if open_txs:
        try:
            return jsonify({'message': 'Successfully retrieved open tranactions',
                            'transactions': [tx.__dict__ for tx in open_txs]})
            response = {
                'message': 'There are no open transactions',
                'blockchain': blockhain.chain}
        except (TypeError, IOError, IndexError) as e:
            return std_response(e, open_txs)

    return jsonify({'message': 'There are no open transactions at this time', 'open transactions': [tx.__dict__ for tx in open_txs]}), 201


@ app.route('/mine', methods=['POST'])
def mine():
    block = blockhain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        response = {'message': 'Block added sucessfully.',
                    'balance': blockhain.get_balance(),
                    'block': dict_block
                    }
        return jsonify(response), 201
        return std_response(dict_block, wallet.public_key != None), 201
    return std_response("Adding block failed.", wallet.public_key != None), 500


@ app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockhain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockhain.get_peer_nodes()
    if nodes:
        response = {
            'message': 'Successfully retrieved nodes',
            'all_nodes': nodes
        }
        return jsonify(response), 200
    response = {
        'message': 'No peer nodes connected at this time'
    }
    return jsonify(response), 201


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    current_nodes = blockhain.get_peer_nodes()
    if values.get('node').lower() in current_nodes:
        responce = {
            'message': 'Node already exist',
            'all_nodes': blockhain.get_peer_nodes()
        }
        return jsonify(responce), 200
    if not values:
        responce = {
            'message': 'No data found.'
        }
        return jsonify(responce), 400
    if not values.get('node'):
        responce = {
            'message': 'No node found.'
        }
        return jsonify(responce), 200
    new_node = values.get('node').lower()
    blockhain.add_peer_node(new_node)
    responce = {
        'message': 'Node added successfully',
        'all_nodes': blockhain.get_peer_nodes()
    }
    return jsonify(responce), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if not node_url.strip() or node_url == None:
        response = {
            'message': 'No node provided'
        }
        return jsonify(response), 400
    blockhain.remove_peer_node(node_url.lower())
    response = {
        'message': f'{node_url} has been successfully deleted',
        'all_nodes': blockhain.get_peer_nodes()
    }
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
