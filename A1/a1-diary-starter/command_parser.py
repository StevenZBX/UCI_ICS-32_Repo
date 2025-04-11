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

def create1(user):
    username = input('Username:\n')
    password = input('Password:\n')
    bio = input('Bio:\n')

    dir = Path(user[1])
    diary_name = user[-1]
    new_diary = dir / (diary_name + '.json')
    new_diary.touch() # Created file in the directory
    path = f'{(user[1])}/{diary_name}.json' # Changed the directory to the user input
    print(path, 'CREATED')
    os.chdir(path)
    new_notebook = Notebook(username, password, bio)
    new_notebook.save(path)


def delete1(user):
    file_path = user[1]
    os.remove(file_path) # Deleted the correspond file
    print(f'{file_path} DELETED')


def print1(user):
    pass


def load1(user):
    pass


def edit1(user):
    print('To edit notebook, you have 5 valid commands ')
    print('-user: Change username')
    print('-pwd: Change password')
    print('-bio: Change bio')
    print('-add: New diary')
    print('-del: Delete the diary in the list')
    
