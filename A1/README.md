Assignment 1 - Diary

You will build an interactive command-based diary program (i.e., you should not read the commands from sys.argv, but use input("") iteratively and parse its contents until the user asks to quit the program using the Q command). A command is a user input that is formatted in a shell-like syntax as below:

[COMMAND] [INPUT] [[-]OPTION] [INPUT]
The INPUT may have whitespaces. However, it should be enclosed with single or double quotation marks in that case. This will help you to handle whitespaces properly, similar to real command line programs. The input command format for INPUTs that have whitespaces looks like this:

[COMMAND] "[SOME INPUT]" [[-]OPTION] "[SOME INPUT]"
To parse commands, you should use the shlex library and familiarize yourself with the split method. Learning how it works differently from Python’s default split method helps you build a robust command parser for your program to handle whitespaces and properly distinguish INPUT from any OPTION in the command.

# Supported Commands
C - Creates a new notebook in the specified directory.
A C command is used to create a new diary notebook in the specified directory. It is structured as below:

C <PATH> -n <DIARY_NAME>
<PATH> is an absolute or relativeLinks to an external site. path to the directory in which the notebook should be created. Since the path is represented differently on Windows and POSIX file systemsLinks to an external site.,  you should not use hard-coded conventions common to one particular operating system (e.g., ‘C:\’) or use string concatenation to build your paths. Instead, you should use the pathlib moduleLinks to an external site. to handle parsing paths and performing any path concatenation. This makes your program functional on any operating system, which is a requirement for this assignment. It might have whitespaces, but in that case, the user must wrap the path between single or double quotation marks, like the example below:
C "/home/john/ics 32/my notebooks" -n my_diary
<DIARY_NAME> is the name of the notebook to create. 
 

After the user enters the C command, your program should prompt the user to collect the following information in order using an empty input statement, i.e., input(""):

username: the username of the notebook user

password: a password to protect access to the notebook

bio: a brief description of the user.

The collected data should be used to create a Notebook object and, using a proper method from the Notebook class, to save it to the specified <PATH> with the <DIARY_NAME>.json as the name. The notebook module has built-in functionality for saving data stored in a Notebook object; all you have to do is form a full path to the location where the notebook should be saved and pass it as an argument to the save_notebook method. After creating the notebook, your program should output the absolute path to the created notebook, whitespace, and the term CREATED.

Example
The following example shows the process of creating a notebook using the C command. Blue lines are the user’s inputs, and the green lines are the program’s output. Note that the first line is the C command, then in the next three lines, the user will input their username, password, and bio, in order. The program makes the notebook path by concatenating the path and the notebook name properly using the pathlib module and appending the .json suffix at the end. Lastly, it makes a profile object using the collected data and stores it in the notebook path. The output is the full path to the notebook file, a whitespace, and the term CREATED.

C "/home/john/ics 32/my notebooks" -n my_diary
John
John123
A junior developer at UCI
/home/john/ics 32/my notebooks/my_diary.json CREATED
If a user attempts to create a file with the same name as an existing file (in the same directory), your program should output ERROR. Additionally, if the intended directory for the new file does not exist, the program should print ERROR. 

D - Deletes a notebook.

The D command will allow the user to delete a notebook. If the user-specified file is not a .json file or the user-specified file does not exist, then the program should print ERROR and wait for corrected input from the user. Once the notebook file has been successfully deleted, your program should print a confirmation that includes the absolute path to the deleted notebook, whitespace, and the term DELETED. For example, if the user inputs the following command:

D /home/algol/ics32/lectures/l1/student.json
The resulting output after deleting the notebook should be:

/home/algol/ics32/lectures/l1/student.json DELETED
O  - Loads an existing notebook
The O command is used by users to load an existing notebook (After they create one using the C command) from a given relative or absolute path. The loaded notebook can then be used to add new diaries, modify the user’s information, and print the user’s diaries. The O command is structured as below:

O <PATH>
After the user inputs the O command, if the path exists and it’s a valid JSON file, your program should expect the user to enter the notebook’s username and password using two empty input("") statements. Then, your program should instantiate a notebook object and use a proper method from the notebook module to load the notebook information. If the username and password entered by the user match the ones in the notebook, your program should print the following, where <Username> and <Password> are the username and password loaded from the notebook:

Notebook loaded.
<Username>
<Bio>
The method that parses the O command should be written in a way that if that:

If the user wants to make changes to the notebook or print their diaries afterward, they shouldn't be asked for the notebook path again. Your program should use the path to the loaded notebook when saving changes.
The loaded notebook must not be loaded anywhere else. The only place that loading occurs is in the O command. This means you should devise a way to preserve the notebook object you create and reuse it when necessary. You are not allowed to use global variables to do so.
E  - Edits the loaded notebook file
The E command can be used by the user after using the C or O command to modify the notebook information. If the E command is issued before any C command or O command is issued, the program should print ERROR. It supports any combination of the following options:

-usr [USERNAME]

-pwd [PASSWORD]   

-bio [BIO] 

-add [NEW DIARY]

-del [0-indexed ID of the Diary to delete] 

The following commands are examples of how the E command can be used.

# Changes the username to John and the password to 123 456
E -usr John -pwd "123 456"

# Adds a diary and removes the first diary in the notebook
E -add "I had such a cool day at Six Flags with my friends" -del 0
Changes to the notebook must be saved after the execution of each option. If the operation of an option results in an error, you should 🛑 stop executing the options from that point on rather than continue processing options. For instance, if the third option causes an error, options 1 and 2 should run, and option 3 fails; the rest of the options should not be executed. In any problematic case, ERROR should be printed after the processing the acceptable options. 

P  - Print the loaded notebook’s information
The P command can be used by the user after using the C or O command to print the notebook information. Like the E command, the P command should not be issued before any C or O command is issued. If it is, the program should print ERROR. It supports any combination of the following options:

-usr Prints the username stored in the loaded notebook object

-pwd Prints the password stored in the loaded notebook object

-bio Prints the bio stored in the loaded notebook object

-posts Prints all diaries stored in the notebook object with their ID (0-indexed)

-post [ID] Prints post identified by ID (0-indexed)

-all Prints all content stored in the loaded notebook object

 

Like the E command, the P command should stop execution upon reaching a problematic option. Your program should print ERROR after printing the output for any successfully processed options.

Q - Quit the program
If the user enters Q at any point, your program should quit.

