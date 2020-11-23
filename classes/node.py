from verification import Validation
from blockchain import Blockchain
from uuid import uuid4


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'Jason'
        self.blockchain = Blockchain(self.id)

    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        print("_"*20)
        for block in self.blockchain.chain:
            print(f"Blockchain index {block.index}:{block.__dict__}")
        else:
            print("-"*20)

    def get_transaction_value(self):
        """Returns user input for requested transaction

        Args:
        sender(string)
        recipient(string)
        amount(int)

        Returns:
        value(int)
        """
        owner_balance = self.blockchain.get_balance()
        amount = float(input("How many coins would you like to send? "))
        if amount > owner_balance:
            return (False, round(amount, 2))
        recipient = input(
            f"Whom would you like to send these {amount} coins: ")
        return (recipient, amount)

    def listen_for_blockchain(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please Choose")
            print("1: Add transaction")
            print("2: Output the Blockchain blocks")
            print("q: Quit")
            print("3: Mine Block")
            print("4: Verify transactions")
            print("t: show open transactions")

            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if not recipient:
                    print(f""" *WARNING*
        You dont have enough to sent {amount} coins """)
                    continue
                if self.blockchain.add_value(recipient, self.id, amount=amount):
                    print(f"""{'*'*20}
                            Transaction added succesfully
                            {'*'*20}""")
                else:
                    print("Failed to add transation")

            elif user_choice == '2' and len(self.blockchain.chain) > 0:
                self.print_blockchain_elements()
                continue
            elif user_choice == 'q':
                waiting_for_input = False
            elif user_choice == '3':
                self.blockchain.mine_block()
            elif user_choice == 't':
                print(self.blockchain.open_transactions)
            elif user_choice == '4':
                if Validation.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions valid")
                else:
                    print("There are invalid transactions")
            else:
                print("Please enter a valid value")
            if not Validation.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid Blockchain!")
                break
            print(
                f"{self.blockchain.hosting_node}'s Balance: {self.blockchain.get_balance()}")

        print("Done!")


node_J_n1 = Node()
node_J_n1.listen_for_blockchain()