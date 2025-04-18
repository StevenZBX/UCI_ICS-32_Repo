# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

import shlex
import command_parser
from notebook import Notebook


def menu() -> None:
    print('This program is for users to manage notebooks.')
    print()
    print('C: create (C <PATH> -n <DIARY_NAME>)')
    print('D: delete (D <Path>)')
    print('O: load (O <Path>)')
    print()
    print("E: edit (E -[Command] '[Content of input]')")
    print('E command ----> (usr, pwd, bio, add, del)')
    print()
    print('P: print (P -[Command])')
    print('P command ----> (usr, pwd, bio, diary [ID], diaries)')
    print()
    print('Note! Please Load a file or Create a file to Edit or Print content!')
    print('Q: quit (Q or q)')
    print('-'*60)


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
    menu()
    check = True
    while check:
        user = shlex.split(input('Input Command: '))
        print()
        if user[0].upper() == 'Q':
                check = False
                print('Goodbye!')
        elif len(user) < 2:
            print('ERROR')
        else:
            if user[0].upper() not in command_lst_file and user[0].upper() not in command_lst_content:
                print('Invalid command!')
            elif user[0].upper() in command_lst_file:
                    try:
                        path, notebook = command_file(user)
                    except:
                        print("Invalid File!")
            elif user[0].upper() in command_lst_content:
                try:
                    command_content(user, path, notebook)
                except NameError:
                    print('You did not load or create a file!')
                except ValueError:
                    print('Input an integer to print specific diary!')
        print('-'*60)


if __name__ == "__main__":
    main()