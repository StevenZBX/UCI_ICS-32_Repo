# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906


import command_parser
import notebook
from pathlib import Path
import os
import json

def menu():
    print('This program is for manage notebooks for users')
    print('You can do these following with the format [COMMAND] [INPUT] [[-]OPTION] [INPUT]:')
    print('Here is an example: C "/home/Steven/ics 32/my notebooks" -n my_diary')
    print('C: create')
    print('D: delete')
    print('O: load')
    print('E: edit')
    print('P: print')
    print('Q: quit')
    


def command():
    if user.upper() == 'C':
        command_parser.create1()
    elif user.upper() == 'D':
        command_parser.delete1()
    elif user.upper() == 'P':
        command_parser.print1()
    elif user.upper() == 'E':
        command_parser.edit1()
    elif user.upper() == 'O':
        command_parser.load1()


if __name__ == "__main__":
    command_lst = ['C', 'D', 'E', 'O', 'P', 'Q']
    menu()
    user = input("How can I help you?\n")
    user_list = user.split()
    print(user_list)

    check  = True
    while check:
        if user.upper() == 'Q':
            check = False
            print('Goodbye! Have a nice day')
        elif user.upper() not in command_lst:
            print('Invalid command!')
            user = input('Please choose agagin')
            command()
        else:
            command()
        
