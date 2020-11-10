# python blockchain.py to run or the green arrow up and to the right
# https://pro.academind.com/courses/767953/lectures/13912811
blockchain = []


def blockchain_len():
    if len(blockchain) > 0:
        return True
    else:
        return False


def prev_blockchain_value():
    """ This function returns the last Block Chain value"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_user_tx_amount():
    return float(input("Enter transaction amount: "))


def user_choice():
    user_input = input('Your choice: ')
    return user_input


# def choices():
#     print(""" Please choose
#     1: Add a new transaction
#     2: Output the blocks
#     3: Manipulate
#     4: Quit
#     5: BlockChain
#      """)


def add_value(trans_amnt):
    """Append a new value as well as the last one 

        Arguments:
        :trans_amnt: Amount to be added to Block Chain.
        :last_trans: Last value added to Block Chain.
    """
    if len(blockchain) < 1:
        blockchain.append([trans_amnt])
    else:
        blockchain.append([prev_blockchain_value(), trans_amnt])


def validate_chain():
    """ 
    Validate_chain checks to see if the last value is entered into the blockchain is in the first element. This prevents any manipulation of the chiain because any manipulation will not be in the previous position of the blockchain.
    """
    is_valid = True
    for idx in range(len(blockchain)):
        # range starts its count from 0 to the penultimate number in the range
        if idx == 0:
            continue
        elif blockchain[idx][0] != blockchain[idx - 1]:
            is_valid = False
    return is_valid


def bc_elements():
    for block in blockchain:
        print(block)


keep_going = True

while keep_going:
    """
    Will run forever because there is nothing changing this to 'False'
    """
    print("""
    1: Add a new transaction
    2: Output the blocks
    3: Manipulate
    4: Quit
    5: BlockChain
     """)
    the_choice = user_choice()
    if the_choice == '1':
        tx_amount = get_user_tx_amount()
        add_value(tx_amount)
    elif the_choice == '2':
        if blockchain_len():
            bc_elements()
        else:
            print("There are no blocks to show")
            continue
    elif the_choice == '3':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif the_choice == '4':
        keep_going = False
    elif the_choice == '5':
        print(blockchain)
    else:
        print("Invalid choice. Please choice 1 - 4")
    if not validate_chain():
        bc_elements()
        print("__"*30)
        print("Invalid Blockchain!")
        break

else:
    print("User left")
