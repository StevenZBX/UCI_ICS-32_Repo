# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

from command_parser import *

def welcome():
    print('Welcome, this is a simple file management')
    print('You can do')
    print('C: create')
    print('D: delete')
    print('O: load')
    print('E: edit')
    print('P: print')
    print('Q: quit')
    

def user():
    user = input('What do you want to do?\n')
    return user

def check(user):
    if user in command_dic.keys():
        pass
    else:
        print('Its not a valid command!')
        user()
    
    

if __name__=="__main__":
    command_dic = {"C": 'create', "D": "delete", "O": "load", "E": "edit", "P": "print", "Q": "quit"}
    welcome()
    check(user = user())
