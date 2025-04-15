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
    print('This program is for users to manage notebooks.')
    print('C: create (C <PATH> -n <DIARY_NAME>)')
    print('D: delete (D <Path>)')
    print('O: load (O <Path>)')
    print("E: edit (E -[Command] '[Content of input]')")
    print('P: print (P -[Command] [Content of file])')
    print('Q: quit (Q or q)')
    print('Note! Please Load a file or Create a file to Edit or Print content!')


def command():
    if user[0].upper() == 'C':
        command_parser.create1(user)
    elif user[0].upper() == 'D':
        command_parser.delete1(user)
    elif user[0].upper() == 'O':
        command_parser.load1(user)
    elif user[0].upper() == 'E' or user[0].upper == 'P':
        print('Error, please load a file or create a file')


if __name__ == "__main__":
    command_lst = ['C', 'D', 'E', 'O', 'P', 'Q']
    menu()
    check = True
    while check:
        user = shlex.split(input('How can I help you? '))
        if user[0].upper() == 'Q':
                check = False
                print('Goodbye!')
        elif len(user) < 2:
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
# E -usr Steven -pwd "123 456"
# E -add "I had such a cool day at Six Flags with my friends"