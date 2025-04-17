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


def edit_menu() -> None:
    print('To edit notebook, you have 5 valid commands')
    print('-user: Change username')
    print('-pwd: Change password')
    print('-bio: Change biography')
    print('-add: Add diary')
    print('-del: Delete the diary in the list')


def print_menu() -> None:
    print('To print notebook, you have 6 valid commands')
    print('-usr: Printing username')
    print('-pwd: Printing password')
    print('-bio: Printing biography')
    print('-diaries: Printing all diaries in notebook')
    print('-diary [ID]: Printing specific diary in the notebook')
    print('-all: Printing all content in the notebook')


def edit1(notebook, user, path) -> None:
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
                    print('Deleted')
                    notebook.save(path)
                else:
                    print('Error: Not Found!')
        else:
            print('Error: Invalid Command!')


def print1(notebook, user) -> None:
    print_list = ['-usr', '-pwd', '-bio', '-diaries', '-diary', '-all']
    user.remove('P')
    for index in range(len(user)):
        if user[index] in print_list: # action for printing
            if user[index] == '-usr':
                print('Username:', notebook.username)
            elif user[index] == '-pwd':
                print('Password:',notebook.password)
            elif user[index] == '-bio':
                print('Biography:',notebook.bio)
            elif user[index] == '-diaries':
                diaries = notebook.get_diaries()
                print('All diaies:')
                sequence = 0
                for diary in diaries:
                    time = datetime.fromtimestamp(diary.timestamp).strftime("%Y-%m-%d %H:%M:%S") # convert timestamp to readable time
                    print(f'{sequence}. ({time}): {diary.entry}')
                    sequence += 1
            elif user[index] == '-diary':
                diary_index = int(user[index+1])
                current_diary = notebook.get_diaries()[diary_index]
                time = datetime.fromtimestamp(current_diary.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                print('Diary:')
                print(f'({time}) {current_diary.entry}') 
            elif user[index] == '-all':
                print('Username:', notebook.username)
                print('Password:',notebook.password)
                print('Biography:',notebook.bio)
                diaries = notebook.get_diaries()
                print('All diaies:')
                sequence = 0
                for diary in diaries:
                    time = datetime.fromtimestamp(diary.timestamp).strftime("%Y-%m-%d %H:%M:%S") # convert timestamp to readable time
                    print(f'{sequence}. ({time}): {diary.entry}') #
                    sequence += 1
        elif user[index].isnumeric():
            pass
        else:
            print('Error: Invalid command!')


def create1(user) -> tuple[str, Notebook]:
    username = input('Username: ')
    password = input('Password: ')
    bio = input('Biography: ')

    dir = Path(user[1])
    diary_name = user[-1]
    new_diary = dir / Path(diary_name + '.json')
    new_diary.touch() # Created file in the directory
    path = f'{(user[1])}/{diary_name}.json' # Changed the directory to the user input
    print(path, 'CREATED')
    new_notebook = Notebook(username, password, bio)
    new_notebook.save(path)

    return path, new_notebook

def delete1(user) -> None:
    file_path = user[1]
    os.remove(file_path) # Deleted the correspond file
    print(f'{file_path} DELETED')


def load1(user) -> tuple[str, Notebook]:
    path = user[1]
    notebook = Notebook('','','')
    notebook.load(path)
    name = input('Username: ')
    pwd = input('Password: ')
    if name == notebook.username and pwd == notebook.password:
        print('Notebook loaded.')
        print(notebook.username)
        print(notebook.bio)
        return path, notebook
    else:
        notebook.save(path)
        print('Error: Invalid username or password')
        load1(user)
