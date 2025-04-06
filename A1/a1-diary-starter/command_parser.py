# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

import shlex

def parse_command(line):
    try:
        tokens = shlex.split(line)
    except ValueError:
        return None, {}, "ERROR"

    if not tokens:
        return None, {}, "ERROR"

    command = tokens[0].upper()
    args = tokens[1:]

    options = {}
    i = 0
    while i < len(args):
        token = args[i]
        if token.startswith('-'):
            if i + 1 >= len(args):
                return None, {}, "ERROR"
            options[token] = args[i + 1]
            i += 2
        else:
            if "main_arg" not in options:
                options["main_arg"] = token
            else:
                options["extra_arg"] = token
            i += 1

    return command, options, None
