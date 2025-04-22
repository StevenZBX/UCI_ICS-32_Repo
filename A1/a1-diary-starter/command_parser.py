# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

from datetime import datetime
from notebook import Diary
from notebook import Notebook
from pathlib import Path
import os


def edit1(notebook, user, path) -> None: # Command for editing notebook obejct, when the command finished, the revision will save in the notebook
    edit_list = ['-usr', '-pwd', '-bio', '-add', '-del']
    user.remove('E')
    for index in range(0, len(user),2):
        command = user[index]
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
                new_diary = Diary(user[index+1])
                notebook.add_diary(new_diary)
                notebook.save(path)
            elif command == '-del':
                revise_diary = notebook.del_diary(int(user[index+1]))
                notebook.save(path)
                if revise_diary:
                    notebook.save(path)
                else:
                    print('ERROR')
        else:
            print('ERROR')


def print1(notebook, user) -> None: # Command for printing content of notebook obejct
    try:
        print_list = ['-usr', '-pwd', '-bio', '-diaries', '-diary', '-all']
        user.remove('P')
        for index in range(len(user)):
            if user[index] in print_list: # action for printing
                if user[index] == '-usr':
                    print(notebook.username)
                elif user[index] == '-pwd':
                    print(notebook.password)
                elif user[index] == '-bio':
                    print(notebook.bio)
                elif user[index] == '-diaries':
                    diaries = notebook.get_diaries()
                    sequence = 0
                    for diary in diaries:
                        print(f'{sequence}: {diary.entry}')
                        sequence += 1
                elif user[index] == '-diary':
                    diary_index = int(user[index+1])
                    current_diary = notebook.get_diaries()[diary_index]
                    print('Diary:')
                    print(f'{current_diary.entry}') 
                elif user[index] == '-all':
                    print(notebook.username)
                    print(notebook.password)
                    print(notebook.bio)
                    diaries = notebook.get_diaries()
                    sequence = 0
                    for diary in diaries:
                        print(f'{sequence}. {diary.entry}')
                        sequence += 1
            elif user[index].isnumeric():
                pass
            else:
                print('ERROR')
    except IndexError:
        print('ERROR')


def create1(user) -> tuple[str, Notebook]: # Command for creating a new notebook obejct, when the notebook created, it will load automatically
    username = input()
    password = input()
    bio = input()

    dir = Path(user[1])
    diary_name = user[-1]
    new_diary = dir / Path(diary_name + '.json')
    new_diary.touch() # Created file in the directory
    print(new_diary, 'CREATED')
    new_notebook = Notebook(username, password, bio)
    new_notebook.save(new_diary)

    return new_diary, new_notebook

def delete1(user) -> None: # Command for deleting a file in the specifc path
    file_path = user[1]
    os.remove(file_path) # Deleted the correspond file
    print(f'{file_path} DELETED')


def load1(user) -> tuple[str, Notebook]: # Command for loading a notebook in the path
    path = user[1]
    notebook = Notebook('', '', '')
    notebook.load(path)
    name = input()
    pwd = input()
    if name == notebook.username and pwd == notebook.password: # when the username and password is correct, the notebook will load
        print('Notebook loaded.')
        print(notebook.username)
        print(notebook.bio)
        return path, notebook
    else: # otherwise, the notebook will close and repeat to ask username and password
        notebook.save(path)
        print('ERROR')
        load1(user)
