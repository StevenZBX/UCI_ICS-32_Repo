# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

from notebook import Notebook
from pathlib import Path
import shlex
import os
import json


def edit1(notebook, user, path):
    # print('To edit notebook, you have 5 valid commands ')
    # print('-user: Change username')
    # print('-pwd: Change password')
    # print('-bio: Change bio')
    # print('-add: Add diary')
    # print('-del: Delete the diary in the list')
    edit_list = ['-usr', '-pwd', '-bio', '-add', '-del']
    user.remove('E')
    print(user)
    for index in range(0, len(user),2):
        command = user[index]
        print(user[index])
        if command in edit_list: # action for editing
            if command == '-usr':
                notebook.username = user[index+1]
                notebook.save(path)
            elif command == '-pwd':
                notebook.password = user[index+1]
                notebook.save(path)
            elif command == '-bio':
                notebook.bio = user[index+1]
                notebook.save(path)
            elif command == '-add':
                notebook.add_diary(user[index+1])
                notebook.save(path)
            elif command == '-del':
                new_diary = notebook.del_diary(int(user[index+1]))
                notebook.save(path)
                if new_diary:
                    print('Deleted')
                    notebook.save(path)
                else:
                    print('Error: Not Found!')
        else:
            print('Error: Invalid Command!')


def print1(user):
    print_list = ['-usr', '-pwd', '-bio', '-diaries', '-diary', '-all']
    user.remove('P')
    for command in user:
        if command in print_list: # action for printing
            if command == '-usr':
                pass
            elif command == '-pwd':
                pass
            elif command == '-bio':
                pass
            elif command == '-diaries':
                pass
            elif command == '-diary':
                pass
            elif command == '-all':
                pass
        else:
            print('Error: Invalid command!')


def create1(user):
    username = input()#'Username: '
    password = input()#'Password: '
    bio = input()#'Bio: '

    dir = Path(user[1])
    diary_name = user[-1]
    new_diary = dir / Path(diary_name + '.json')
    new_diary.touch() # Created file in the directory
    path = f'{(user[1])}/{diary_name}.json' # Changed the directory to the user input
    print(path, 'CREATED')
    new_notebook = Notebook(username, password, bio)
    new_notebook.save(path)

    # New branch for user to edit or print file, or back to the previous choices
    notebook = Notebook('','','')
    notebook.load(path)
    check = True
    while check:
        user = shlex.split(input('Editing or Printing the content of file (input Q to back previous choice): '))
        if user[0].upper() == 'E':
            edit1(notebook, user, path)
        elif user[0].upper() == 'P':
            print1(user)
        elif user[0].upper() == 'Q':
            notebook.save(path)
            check = False
    

def delete1(user):
    file_path = user[1]
    os.remove(file_path) # Deleted the correspond file
    print(f'{file_path} DELETED')


def load1(user):
    path = user[1]
    
    notebook = Notebook('','','')
    notebook.load(path)
    name = input()#'Username: 's
    pwd = input()#'Password: '
    if name == notebook.username and pwd == notebook.password:
        print('Notebook loaded.')
        print('Username:', notebook.username)
        print('Bio:', notebook.bio)
    else:
        notebook.save(path)
        print('Error: Invalid username or password')
        load1(user)
    # # Editing or Printing content after loading file
    check = True
    while check:
        user = shlex.split(input('Editing or Printing the content of file (input Q to back previous choice): '))
        if user[0].upper() == 'E':
            edit1(notebook, user, path)
        elif user[0].upper() == 'P':
            print1(user)
        elif user[0].upper() == 'Q':
            notebook.save(path)
            check = False
