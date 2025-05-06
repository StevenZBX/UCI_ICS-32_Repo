# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

import shlex
import command_parser
from notebook import Notebook


def command_file(user) -> tuple[str, Notebook]:
    if user[0].upper() == 'C':
        path, notebook = command_parser.create1(user)
        return path, notebook
    elif user[0].upper() == 'O':
        path, notebook = command_parser.load1(user)
        return path, notebook

def command_content(user, path, notebook) -> None:
    if user[0].upper() == 'D':
        command_parser.delete1(user)
    elif user[0].upper() == 'E':
        command_parser.edit1(notebook, user, path)
    elif user[0].upper() == 'P':
        command_parser.print1(notebook, user)


def main() -> None:
    command_lst_file = ['C', 'O']
    command_lst_content = ['D', 'E', 'P']
    check = True
    path = None
    notebook = None
    while check:
        user = shlex.split(input())
        if user[0].upper() == 'Q':
                check = False
        elif len(user) < 2:
            print('ERROR')
        else:
            if user[0].upper() not in command_lst_file and user[0].upper() not in command_lst_content:
                print('ERROR')
            elif user[0].upper() in command_lst_file:
                    try:
                        path, notebook = command_file(user)
                    except:
                        print("ERROR")
            elif user[0].upper() in command_lst_content:
                try:
                    command_content(user, path, notebook)
                except NameError:
                    print('ERROR')
                except ValueError:
                    print('ERROR')


if __name__ == "__main__":
    main()