# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906


from command_parser import parse_command
from notebook import Notebook
from pathlib import Path
import os
import json

def main():
    loaded_notebook = None
    loaded_path = None

    while True:
        try:
            user_input = input("")
        except EOFError:
            break

        command, opts, err = parse_command(user_input)

        if err:
            print("ERROR")
            continue

        if command == "Q":
            break

        elif command == "C":
            path_str = opts.get("main_arg")
            name = opts.get("-n")

            if not path_str or not name:
                print("ERROR")
                continue

            path = Path(path_str)
            if not path.exists() or not path.is_dir():
                print("ERROR")
                continue

            file_path = path / f"{name}.json"
            if file_path.exists():
                print("ERROR")
                continue

            username = input("")
            password = input("")
            bio = input("")

            nb = Notebook()
            nb.create_profile(username, password, bio)
            nb.save_notebook(str(file_path.resolve()))

            loaded_notebook = nb
            loaded_path = str(file_path.resolve())
            print(f"{loaded_path} CREATED")

        elif command == "D":
            target_path = opts.get("main_arg")
            if not target_path or not target_path.endswith(".json"):
                print("ERROR")
                continue

            file = Path(target_path)
            if not file.exists():
                print("ERROR")
                continue

            try:
                file.unlink()
                print(f"{str(file.resolve())} DELETED")
            except Exception:
                print("ERROR")

        elif command == "O":
            target_path = opts.get("main_arg")
            if not target_path or not target_path.endswith(".json"):
                print("ERROR")
                continue

            file = Path(target_path)
            if not file.exists():
                print("ERROR")
                continue

            username = input("")
            password = input("")

            try:
                nb = Notebook()
                nb.load_notebook(str(file.resolve()))
                if nb.username != username or nb.password != password:
                    print("ERROR")
                    continue

                loaded_notebook = nb
                loaded_path = str(file.resolve())
                print("Notebook loaded.")
                print(nb.username)
                print(nb.bio)

            except Exception:
                print("ERROR")

        elif command == "E":
            if not loaded_notebook or not loaded_path:
                print("ERROR")
                continue

            try:
                for opt, val in opts.items():
                    if opt == "-usr":
                        loaded_notebook.username = val
                    elif opt == "-pwd":
                        loaded_notebook.password = val
                    elif opt == "-bio":
                        loaded_notebook.bio = val
                    elif opt == "-add":
                        loaded_notebook.add_entry(val)
                    elif opt == "-del":
                        idx = int(val)
                        if 0 <= idx < len(loaded_notebook.diary_entries):
                            loaded_notebook.remove_entry(idx)
                        else:
                            print("ERROR")
                            break
                    else:
                        print("ERROR")
                        break
                loaded_notebook.save_notebook(loaded_path)

            except Exception:
                print("ERROR")

        elif command == "P":
            if not loaded_notebook:
                print("ERROR")
                continue

            try:
                for opt in opts:
                    if opt == "-usr":
                        print(loaded_notebook.username)
                    elif opt == "-pwd":
                        print(loaded_notebook.password)
                    elif opt == "-bio":
                        print(loaded_notebook.bio)
                    elif opt == "-posts":
                        for i, post in enumerate(loaded_notebook.diary_entries):
                            print(f"{i}: {post}")
                    elif opt == "-post":
                        idx = int(opts[opt])
                        if 0 <= idx < len(loaded_notebook.diary_entries):
                            print(loaded_notebook.diary_entries[idx])
                        else:
                            print("ERROR")
                            break
                    elif opt == "-all":
                        print(loaded_notebook.username)
                        print(loaded_notebook.password)
                        print(loaded_notebook.bio)
                        for i, post in enumerate(loaded_notebook.diary_entries):
                            print(f"{i}: {post}")
                    else:
                        print("ERROR")
                        break

            except Exception:
                print("ERROR")

        else:
            print("ERROR")

if __name__ == "__main__":
    main()
