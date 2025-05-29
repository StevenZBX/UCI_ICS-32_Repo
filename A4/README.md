## Assignment 4

In this assignment that consists of three parts, you will use your knowledge about HTTP requests, Tkinter events, as well as higher-order functions to complete three tasks.

 

Part 1) HTTP Requests
In this part, your goal is to write a test module that will send URLs to the PyBookmarker Online server over HTTP. Some starter code has been provided for you in the a4_p1.py module. You may also want to take a peek at the updated bookmark_server.py module to understand how the messages you send will be received and stored on the server. You can download the starter files for this part of the assignment from here Download here.

File Descriptions
note.py: This module contains the base class for the PyBookmarker program. It provides file read and write access. You have worked with this file in previous labs.
bookmarker.py: This module contains the main class for the PyBookmarker program. It derives from note.py and adds support for bookmark management. You have worked with this file in previous labs.
bookmark_connection.py: This module provides helper functions for managing client and server socket connections.
bookmark_server.py: This module is executable and runs the PyBookmarker Online server.
a4_p1.py: This module is executable and will run the PyBookmarker Online HTTP test client.
Requirements
You should not change the existing function names in a4_p1.py. You are free to add parameters or additional functions if you like, though.
Write at least three simple tests that send URLs over HTTP to the PyBookmarker Online HTTP server.
Part 2) Higher-order Functions
Let’s start this part by seeing an example:

def handle_exception(func, param):
    try:
        return func(param)
    except Exception as ex:
        print(ex)
This function is written by an experienced developer to move repetitive exception handling out of a conditional block and into a single function. The function, handle_exception, is responsible for calling whatever function was passed to the func parameter. The ability to perform this type of operation is foundational to a programming paradigm known as functional programming. At the core of any programming language that supports functional programming is the ability to treat functions as objects, or what is often referred to as 'first-class citizens.' Here is a good description from (Wikipedia)[https://en.wikipedia.org/wiki/Functional_programmingLinks to an external site.]:

In functional programming, functions are treated as first-class citizens, meaning that they can be bound to names (including local identifiers), passed as arguments, and returned from other functions, just as any other data type can.

Python started as a functional programming language, but over time evolved to support the object-oriented features we have been primarily exploring in this class (classes, inheritance, abstraction).

The notion of treating functions as objects can be a bit confusing the first time you are confronted with it. So in this part of the assignment, your goal will be to solidify your understanding of this concept through the application of callbacks. A callback is essentially an operation in which one segment of code hands off responsibility of calling a function to another segment of code. Similar to the example we saw above. Callbacks are also a useful way to support operation between two classes.

Let's look at another callback example...

In this example, there are two classes, Accounting and Communicator. Accounting is responsible for reporting on payouts received. Communicator is responsible for receiving payouts from some hypothetical remote system (we've simulated it with a loop and sleep delay).

The classes communicate with each other using a callback. Go ahead and run the code and study it by following the flow of control.

import time,random

class Accounting:
    def payout(self, amount):
        msg = "Latest Payout: ${:,.2f}".format(amount)
        print(msg)
        

class Communicator:
    def notify(self, pay_report:callable):
        while True:
            pay_report(random.randrange(0, 100))
            time.sleep(3)

a = Accounting()
c = Communicator()

c.notify(a.payout)
For this part, your goal i to update the code provided for you to make use of a callback following the strategies discussed above. You will update the dog feeding program from previous labs so that dog objects notify their calling code when they are hungry, rather than relying on an inquiry from the calling code.

Requirements
You can download a starting code from here Download here. You are free to implement your code however you want, but it must adhere to the following requirements:

In the Dog class, update the hungry method so that it accepts a callable parameter and calls it on some interval (you can use the sleep example above or continue using the random hunger generator.
In the 'main' section, write a function to feed the dog. You will pass this function to the hungry method of the Dog class.
Part 3) Tkinter GUI and Events
Well, it's time to head back to the PyBookmark program. PyBookmark has served us well this quarter, so it's time we return the favor. You will do this by putting a nice shiny graphical interface on top of the Bookmarker.py and Note.py modules!

In this part of the assignment, you will update the Tkinter program provided for you in the a4_p3.py module to complete the requirements listed below. The current module that you can download from here Download hereis nearly complete, but not functional. You will need to take what you have learned about Tkinter, events, and callbacks so far and apply it. The program follows the layout paradigm we use for GUI in this class: a class derived from tkinter.Frame, a draw method to render all graphical elements, and callbacks to support communication between class objects.

Requirements
You are free to implement your code however you want, but it must adhere to the following requirements:

Open Existing *.pbm Files
The PyBookmark file type has been changed to pbm. A method called open_file has already been created. You will need to connect this method to the open menu item in the MainApp class.

Connect Button Events to Callbacks
The Add and Delete URL buttons are in the Footer class, but you will need to receive notifications in the MainApp class when those buttons are clicked. You will accomplish this task by connecting callback functions.

First, in the Footer class, create commands for the delete and add buttons. Assign the add_click method to the add command and the delete_click method to the delete command.
Next, connect the callbacks. Support for callbacks is already in place in the Footer class. So all you will need to do is pass the desired callback functions to the Footer class on instantiation.
Add a URL Text Input Widget
The widgets required to display URLs are already in place. But the current GUI does not have a text widget for typing new URLs. So for this final requirement, you will need to update the Body class to render a Text widget.

The Text widget should be named message_editor, and it should be a member of the Body class.
The Text widget should be added to the message_frame Frame widget that already exists in the Body class.
Files to Submit
You should submit a zip file that has the exact same file structure as below:

├── a4_part1

│   ├── a4_p1.py

│   ├── bookmark_connection.py

│   ├── bookmark_server.py

│   ├── bookmarker.py

│   └── note.py

├── a4_part2

│   └── a4_p2.py

└── a4_part3

    ├── a4_p3.py

    ├── bookmarker.py

    └── note.py
If you downloaded each part’s files separately, compressing the three downloaded folders into a zip file should form the requested file structure.