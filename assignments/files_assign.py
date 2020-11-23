import os.path
from os import path
import json
import pickle


if not path.isfile('practice_file.txt'):
    with open('practice_file.txt', mode='x'):
        pass
# 1. Write file and read from file
# 2 Commented there is also the append to list functionality that will add all items at once
answers_list = list()
# running = True
# while running:
#     user_choice = input("""
#     Please choose:
#         1. input data
#         2. output data
#         q. quit
#     """)
#     if user_choice == '1':
#         user_text = input('Type desired string: ')
#         with open('practice_file.txt', mode='a') as f:
#             f.write(user_text)
#             f.write('\n')
#             answers_list.append(user_text)
#     elif user_choice == '2':
#         with open('practice_file.txt', mode='r') as f:
#             for line in f.readlines():
#                 print(line)
#     elif user_choice == 'q':
#         # with open('practice_file.txt', mode='a') as f:
#         #     for item in answers_list:
#         #         f.write('\n')
#         #         f.write(item)
#         running = False


# 3. Use json

# running = True
# while running:
#     user_choice = input("""
#     Please choose:
#         1. input data
#         2. output data
#         q. quit
#     """)
#     if user_choice == '1':
#         user_text = input('Type desired string: ')
#         answers_list.append(user_text)
#         with open('practice_file.txt', mode='w') as f:
#             f.write(json.dumps(answers_list))
#     elif user_choice == '2':
#         with open('practice_file.txt', mode='r') as f:
#             for line in json.loads(f.read()):
#                 print(line)
#     elif user_choice == 'q':
#         # with open('practice_file.txt', mode='a') as f:
#         #     for item in answers_list:
#         #         f.write('\n')
#         #         f.write(item)
#         running = False


# 4. Pickle
running = True
if not path.isfile('pickle_file.p'):
    with open('pickle_file.p', mode='xb'):
        pass
while running:
    user_choice = input("""
    Please choose:
        1. input data
        2. output data
        q. quit
    """)
    if user_choice == '1':
        user_text = input('Type desired string: ')
        answers_list.append(user_text)
        with open('pickle_file.p', mode='wb') as f:
            f.write(pickle.dumps(answers_list))
    elif user_choice == '2':
        with open('pickle_file.p', mode='rb') as f:
            for line in pickle.loads(f.read()):
                print(line)
    elif user_choice == 'q':
        # with open('practice_file.txt', mode='a') as f:
        #     for item in answers_list:
        #         f.write('\n')
        #         f.write(item)
        running = False
