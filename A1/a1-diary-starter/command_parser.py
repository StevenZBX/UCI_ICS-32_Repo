# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

from pathlib import Path
import shlex
import os
import json

def create1(user):
    dir = Path(user[1])
    diary_name = user[-1]
    new_diary = dir / (diary_name + '.json')
    new_diary.touch()
    os.chdir(user[1])
    print(f'{os.getcwd()}/{diary_name}.json')


def delete1(user):
    file_path = user[1]
    os.remove(file_path)
    print(f'{file_path} DELETED')


def print1(user):
    pass


def load1(user):
    pass


def edit1(user):
    pass


def quit1(user):
    pass