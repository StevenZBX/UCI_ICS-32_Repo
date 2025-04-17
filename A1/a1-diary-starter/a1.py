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
    print()


def command_file():
    if user[0].upper() == 'C':
        path, notebook = command_parser.create1(user)
        return path, notebook
    elif user[0].upper() == 'O':
        path, notebook = command_parser.load1(user)
        return path, notebook

def command_content():
    if user[0].upper() == 'D':
        command_parser.delete1(user)
    elif user[0].upper() == 'E':
        command_parser.edit1(notebook, user, path)
    elif user[0].upper() == 'P':
        command_parser.print1(notebook, user)


if __name__ == "__main__":
    command_lst_file = ['C', 'O']
    command_lst_content = ['D', 'E', 'P']
    menu()
    check = True
    while check:
        user = shlex.split(input())
        if user[0].upper() == 'Q':
                check = False
                print('Goodbye!')
        elif len(user) < 2:
            print('ERROR')
        else:
            if user[0].upper() not in command_lst_file and user[0].upper() not in command_lst_content:
                print('Invalid command!')
            elif user[0].upper() in command_lst_file:
                path, notebook = command_file()
            elif user[0].upper() in command_lst_content:
                try:
                    command_content()
                except NameError:
                    print('You did not load or create a file!')
                except IndexError:
                    print('Incomplete Command!')
        print()


# Prompt for testing
# C "/Users/zbx/Desktop/Spring2025/ICS-32/assignment/A1/a1-diary-starter/test folder" -n notebook
# D "/Users/zbx/Desktop/Spring2025/ICS-32/assignment/A1/a1-diary-starter/test folder/notebook.json"
# O "/Users/zbx/Desktop/Spring2025/ICS-32/assignment/A1/a1-diary-starter/test folder/notebook.json"
# E -usr Steven -pwd "123 456"
# E -add "I had such a cool day at Six Flags with my friends"