# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

import shlex
import command_parser
from notebook import Notebook
from pathlib import Path
import os
import json


def menu():
    print('This program is for manage notebooks for users')
    print('You can do these following with the format [COMMAND] [INPUT] [[-]OPTION] [INPUT]:')
    print('C: create')
    print('D: delete')
    print('O: load')
    print('E: edit')
    print('P: print')
    print('Q: quit')


def command():
    if user[0].upper() == 'C':
        command_parser.create1(user)
    elif user[0].upper() == 'D':
        command_parser.delete1(user)
    elif user[0].upper() == 'P':
        command_parser.print1(user)
    elif user[0].upper() == 'E':
        print('Error, choose a file to load or create a file')
    elif user[0].upper() == 'O':
        command_parser.load1(user)
        if user[0].upper == 'E':
            command_parser.edit1(user)


if __name__ == "__main__":
    command_lst = ['C', 'D', 'E', 'O', 'P', 'Q']
    # menu()
    check = True
    while check:
        user = shlex.split(input())#'How can I help you?\n'
        if user[0].upper() == 'Q':
                check = False
                # print('Goodbye!')
        elif len(user) == 1:
            print('ERROR')
        else:
            if user[0].upper() not in command_lst:
                print('Invalid command!')
                user = input('Please choose again:\n')
                command()
            else:
                command()


# Prompt for testing
# C "/Users/zbx/Desktop/Spring2025/ICS-32/assignment/A1/a1-diary-starter/test folder" -n notebook
# D "/Users/zbx/Desktop/Spring2025/ICS-32/assignment/A1/a1-diary-starter/test folder/notebook.json"
# O "/Users/zbx/Desktop/Spring2025/ICS-32/assignment/A1/a1-diary-starter/test folder/notebook.json"
# E -usr John -pwd "123 456"
# E -add "I had such a cool day at Six Flags with my friends"