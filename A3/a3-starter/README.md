### Assignment 3  Direct Messaging Chat

In assignment 1, you built a useful tool to read, write, delete, and edit files in your personal file system. However, to start to build more interesting programs, we need to be able to branch out and start interacting with programs that other programmers wrote, potentially running on machines all around the world. Think of your favorite social media application; how interesting would an app like Instagram be if we could only post and look at our own photos (it wouldn't be an image sharing app, it would just be a photo library app). In this assignment, we look at how Python sockets can enable you to build some very interesting programs,

For assignment2, you will develop a program that enables a program to send and receive direct messages to another user on the ICS32 distributed social platform (DSP)!. You will then incorporate this module into a graphical user interface (GUI) using Tkinter that should allow any student to communicate with any other student in this class as long as they know each other usernames.

 

To help you get started, the requirements for your final program have been divided into different parts. You are encouraged to follow each part in order. Note that each part can be written and tested independently.

 

Very important: do not wait until near the deadline to start this project, as you will certainly not have time to complete it if you do so, and this project deadline will not be extended. 

Summary of Program Requirements
Write code to support a communication protocol.
Write code to communicate with a server over network sockets
Write code to locally store messages between a user and their contacts
Incorporate your program into a GUI using Tkinter
Program Requirements
In this assignment, you have a lot of flexibility with how you design your program’s user interface. You will not have a validity checker for this assignment, so the input and output of your program are largely up to you. However, there are some conditions:

You must divide your program into at least three modules. Download the starter files here Download here.  
a3.py: Your first module will be the entry point to your program. It will be responsible for importing and using the other modules.  
ds_protocol.py: Your adaptation of the DSP protocol.
ds_messenger.py: Your client to communicate with he server. It should contain all code required to exchange messages with the DSP Server.
Note: Please do not rename the files in the starter files, as it may cause the auto-grader to fail to assess your program.

About the Server
Although sockets are very useful for allowing your program to communicate with a program running on a very distant machine, we intend for you to run a server.py file locally on your machine. This is to simulate a server that could be running on the Internet, allowing two users running their program on different machines to interact.

You can first start the server by running the following command in your terminal, (or running server.py directly in your IDE):

python3 server.py [port1]
port1: This is the port on which your server will run. You can pass in any port you want for this value. The default port with be 3001. 

Important Note: You can choose whatever port you like while developing your program, and this would require you to hardcode whatever value you choose in the code you write to connect to the server. However, your program should be able to connect to a server running on port 3001, since that is where we will run the server in the autograder. 

Upon running the server.py, a directory called store containing a JSON file called users.json will be created for your. You can inspect the way users are stored in this file, but in short, users.json holds a JSON object of user objects associated with distinct user names. Think of users.json as a dictionary of dictionaries (of dictionaries). 

Note: You should run server.py in its own dedicated terminal so that you can run your program that will then connect to and interact with the server.

I think that's all you need to know about the server.py program to get started, Reach out to course staff (on EdStem or in Lab if you are having technical difficulties).

## Part 1: Implement the Direct Messaging Protocol
Much of the ideas behind the work you will need to do to connect to the DSP Server using network sockets are covered in our lectures. If you haven’t been to the lectures, make sure to watch the recording and go over the slides.
To communicate with the server program, your program must implement a protocol capable of sending a few different types of commands over a socket. You will have to write code to connect to the server, implement the protocol to build these commands, and read the responses sent back from the server.  

When communicating with a server using sockets, it is common to establish a protocol for exchanging messages. A protocol is a predefined system of rules to transfer information between two or more systems. You can get inspired by an example of a protocol written for a server-side program here Download here. You may read the file and think how to change it to be used on a client side, since your program is a client to the DSP server.

Your program must support the DSP protocol to communicate successfully with the DSP server. Your protocol handling code should be placed in the ds_protocol.py module. It should include methods to form requests that can be sent to the server, as well as a method to parse any response from the server. All protocol messages must be sent as a JavaScript Object Notation (JSON) string. All responses from the DSP server will be in JSON format as well, which should be converted into a DSPResponse namedtuple.

Supported Operations
authenticate
When a new or existing user needs to communicate with the server, they must send an authenticate request to the server using their username and password and acquire a token that can be used in future requests. The server uses the token to retrieve and return the user’s data. An  authenticate request is a JSON string structured as below:

{"authenticate": {"username": "<USERNAME>","password": "<PASSWORD>"}}
Where the <USERNAME> is the username of the user trying to authenticate, <PASSWORD> is their password. The server will respond with a JSON string structured as below:

{"response": {"type": "ok", "message": "Welcome back,<USERNAME>", "token": "<TOKEN>"}}
Where the type can be ok if the authentication is successful or error if something has gone wrong.

An ok response includes a token value that is your authentication token to acknowledge that you have successfully logged on to the server. This token is only valid if a client is connected to a server. If you authenticate a user and then disconnect from the server, the token will no longer be valid.  You must use this token in all server communication after the initial authenticate request.

An error response includes the error message in the message field.

directmessage
When an authenticated user wants to send a message to another user, they should send a directmessage request to the server. It should be structured as a JSON string like the one below:

{"token":"<TOKEN>", "directmessage": {"entry": "<MESSAGE>","recipient":"<RECEPIENT USERNAME>", "timestamp": "<TIMESTAMP>"}}
Where <TOKEN> is the token received after authenticating the user, <RECEPIENT USERNAME> is the username of the user who will receive the message, and <TIMESTAMP> is the unix timeLinks to an external site. (a float that represents time spent since 1/1/1970 (it uses the Unix epoch). This is standard, and there are built-in methods to convertLinks to an external site. from this value to whatever value you like. The server will respond with a JSON string structured as below:

{"response": {"type": "ok", "message": "Direct message sent"}}
fetch
When an authenticated user wants to retrieve unread messages or their all-time conversation history, they should send a fetch request to the server. It should be structured as a JSON string like the one below:

{"token":"<TOKEN>", "fetch": "<WHAT>"}

Where <TOKEN> is the token received after authenticating the user, and <WHAT> can either be all to retrieve all the messages that the user has ever sent and received or unread to retrieve only the user's unread messages. If <WHAT> is set to unread, the server will respond with a JSON string structured as below:

{
  "response": {
    "type": "ok",
    "messages": [
      {
        "message": "Are you there?!",
        "from": "markb",
        "timestamp": "1603167689.3928561"
      },
      {
        "message": "Text me ASAP",
        "from": "thebeemoviescript",
        "timestamp": "1603167689.3928561"
      }
    ]
  }
}
Otherwise, if <WHAT> is set to all, the server will respond with a JSON string structured as below:

{
  "response": {
    "type": "ok",
    "messages": [
      {
        "message": "Are you there?!",
        "from": "markb",
        "timestamp": "1603167689.3928561"
      },
      {
        "message": "Yeah I just went to grab some water! Jesus!",
        "recipient": "markb",
        "timestamp": "1603167699.3928561"
      },
      {
        "message": "Bzzzzz",
        "from": "thebeemoviescript",
        "timestamp": "1603167689.3928561"
      }
    ]
  }
}
Note that in the case of fetching all,  some messages retrieved from the server have a "recipient" field, while others have a "from" field. This denotes that some messages were sent by the user (outgoing message), and some were sent to the user (incoming message).

Error Handling
There are also a number of possible error response messages that can come from the DS server (e.g. trying to join with the incorrect password for an already-existing users). You can discover some of these errors by looking at the server.py code provided to you, or you can play around with problematic JSON requests.

Forming Requests
In your Python code, you will treat JSON messages as type strings. In the snippets above, you will likely need to replace the hard-coded values (e.g., ohhimark, password123, etc.) with the variables in your program that store the actual data you intend to send to the DSP server. There are many ways to do this, but you should focus your efforts on using the string formatting functions found in the Python Standard Library that we mentioned in the lecture.

Parsing Server Response
To process the messages from the DSP server, you will need to adapt the following function, which can be found in your starter code, to reduce some of the extra work of parsing strings:

import json
from collections import namedtuple

# Create a namedtuple to hold the values we expect to retrieve from json messages.
ServerResponse = namedtuple('ServerResponse', ['foo','baz'])

def extract_json(json_msg:str) -> ServerResponse:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return ServerResponse(foo, baz)

# Example Test
json_msg = '{"foo":"value1", "bar": {"baz": "value2"}}'
print(extract_json(json_msg))

>>> ServerResponse(foo='value1', baz='value2')
The code above is a starting point. You must replace ‘foo’, ‘baz’, etc., with the keys represented by the keys used in the DSP protocol. You are also free to modify this code in any way you want!

Getting Started Example
A typical exchange between a program and a DSP server might look like the following:

join_msg = '{"join": {"username": "mike_zimmermann","password": "password123"}}'

send = client.makefile('w')
recv = client.makefile('r')

send.write(join_msg + '\r\n')
send.flush()

resp = recv.readline()
print(resp)
	
>>> b{"response": {"type": "ok", "message": "Welcome back, ohhimark", "token": "07da3ddc-6b9a-4734-b3ca-f0aa7ff22360"}}
Writing a Test
When your code is complete, write a small test program to verify that your messages are processed as expected. Your program should import your module (e.g., import ds_protocol, if you are extending your ds_protocol module) and call the code you have written with a few test messages. You can use the messages provided as examples above or create a few of your own as test cases. You can name your test whatever you like, but it should be prepended with the word test_:

test_ds_message_protocol.py
Once your test program is complete, you can move on to the next part of the assignment.

 

## Part 2: The DS Direct Messenger Module
Now that you have a functioning protocol, you can write your message send and retrieve code. The first thing you will do is complete the direct messenger module. Your module must adhere to the following rules:

It must be named ds_messenger.py

It must implement the following classes and methods

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.sender = None
    self.message = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    # more code should go in here
		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    pass
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass
You can add as many supporting methods as you need to either of these classes. A program that imports your module should be able to call the required functions to exchange messages with the DS server. These required methods alone should be sufficient to communicate with the DS Server. Y

Writing a Test
Once again, when your code is complete, write a small test program to verify that your ds_messenger module is functioning correctly. You can name your test whatever you like, but it should be prepended with the word test_:

test_ds_messenger.py
Once your test program is complete, you can move on to the next part of the assignment. You are free to run the server to test this module as ds_messenger needs server communication.

## Part 3: Store Messages Locally
Some of the data your program uses should be preserved across multiple users. To complete this feature, you can either implement your own data storage code or, what can be more straightforward, extend the notebook module to support serializing new data.

Your program should be able to store message data locally so that when the program starts, it does not have to connect to the DSP server to display previously retrieved messages. Your program should also store recipient data locally so that your user does not have to add the same recipients each new time the program is run (for instance, you can create a new attribute in Notebook containing a list of contacts). It’s OK if you require a user to first load their notebook (or any other custom file format you build) before displaying data. The important thing here is to NOT require an internet connection to get messages that were already previously retrieved.

However you handle this requirement, after using your program once, all recipients who were previously added and all the messages that were previously retrieved by the user, should appear in your GUI (see Part 4) when it starts at any subsequent use.

After implementing this part, you might be wondering: why do I ever need to call retrieve_all() if I am saving the messages locally? Answer: sometimes you might not have the for a user that a server does in fact have. Imagine you were joining with a user from a different machine (with an entirely different file system). Or imagine you accidentally deleted the .dsu file for a user. Therefore, it is still important to be able to successfully call retrieve_all() to retrieve any message histories a server might have for a user. Retrieving message histories from the server and retrieving messages histories you store locally both have their time and place.

## Part 4: The Graphical User Interface
The final part of the assignment will be to write a graphical user interface (GUI) for your module using Tkinter. You are free to implement the interface however you like or to adapt the Tkinter GUI starter code that you are given below.

There are many ways to create a graphical interface for a direct messaging program. You are not required to follow the example below. However, if you are unsure where to start, the following wireframe should point you in the right direction.
In the wireframe model presented above, there are 5 widgets which are responsible for all of the input and output in the program:

On the left is a treeview widget that displays all of the DS users that have sent you messages. Selecting a user must display the messages that they have sent in (2).

On the upper right is the display widget that contains the messages sent by the user selected in (1).

On the lower right is the text input widget where new messages are written.

The ‘Add User’ button adds new contacts (recipients) to receive direct messages.

The ‘Send’ button sends the message entered in (3) to the user selected in (1).

 

A small help: The layout used in this wireframe is nearly identical to the layout provided to you as an example code in this link Download example code in this link. You may reuse this existing code to save you some steps, but if you decide to use this code instead of writing your own interface from scratch, you must to modify it a bit (for instance by moving some options around, adding new options, or a new design, reconfiguring the way that the messages are printed by adding color, etc.) and you also need to finish implementing it, as the provided code is not fully operational.


## In addition to the requirements described above, there are a few other tasks you must do to complete the assignment:

Your GUI must automatically retrieve new messages while the program runs (see the after method to create timed events in tkinter, as we covered in week 4).

Your conversations must be visually separated in some way between the different students (e.g., left/right align, color, identifier, etc; if you are using a tkinter text widget, look for how to use tags with the text insert methods).

Selecting a new contact in the treeview should display any recent messages with that contact in the message window (e.g. you will need to clear the text box contents and then insert the previous messages of the selected user).

Testing
This blog postLinks to an external site. is a good guide for writing pytest-compatible test cases. Since the rubric item is auto-graded, you must ensure your test cases are written in a pytest-compatible format. That means all your test files should start with test_ and inside your test files, each test case method should start with test_ e.g., test_the_name_of_the_functionalIty_being_tested .

Your test cases will be evaluated based on how much of the code in the tested modules are being tested by your test cases. To get that idea, you can install the coverage library through pip install coverage. Then, run the following commands in the folder where your test cases are:

pip install pytest
coverage run -m --branch pytest .
coverage report -m
Your output is gonna be a table that shows a percentage of lines covered by your test cases as well as the covered branches. Please read this blog post to understand the difference between these two metrics:

https://about.codecov.io/blog/line-or-branch-coverage-which-type-is-right-for-youLinks to an external site.

If you have any questions or need clarifications, please attend the lab sections or LAs office hours.

Demo Video
You should record a demo video to showcase the functionality of your program. If you’re using a Mac, you can use this guideLinks to an external site. to record the video. On Windows, you can use free software, such as OBSLinks to an external site., to record your demo.

The initial state of the program when demo is that there are no chats with any users. Please follow the below steps in your recorded video:

Run the server.
Run your program and log in as Alice. Keep Alice’s window open. 
Run your program and log in as Bob. Keep Bob’s window open side-by-side to Alice’s window.
Send a message from Alice to Bob and show that Bob has received the message. 
Send a message from Bob to Alice and show that Alice has received the message.
Stop the server
Close both Alice and Bob’s windows.
Keep the server stopped (Do not run it again) and run your program again as Alice. Alice’s window should show Bob in the contact list.
Select Bob from the contact list. Alice’s with Bob should be displayed.
Attempt to send a message to Bob. The message should not be sent, should not be added to the GUI, and an error message should be displayed on the GUI.
What to submit?
1. Submit all your .py files in a zip file on Gradescope.

2. Submit a demo video of your application on Canvas.

You are free to design your code as you wish as long as you respect the assignment's requirements above.

You must put your main() function (and obviously your if __name__ == "__main__": code) inside the a4.py file. 

 

Important reminder notes: as usual in a professional code development scenario, you are required: to keep track of your development using git with regular commits, as we previously saw in the quarter; to respect PEP8 Python coding styles; to add a simple but descriptive README file; and to deal with possible exceptions and errors that may happen. You will not get additional points for respecting these software development requirements, but penalties in the assignment are associated with not following them, as you would be producing lower-quality software.

1. On the coding style: before submission, make sure to check your style and possible code mistakes using pycodestyle and pylint as seen in lecture, and make all the necessary changes, including in any starter code provided to you, as they include simple style issues for you to correct. It should be simple to fix most of the code issues, thus respecting PEP8, if you address the pycodestyle and pylint errors and warnings, thus avoiding any penalty. You do not have to worry about correcting style issues in server.py.  

2. On testing: it is expected that your assignment 3 code will include unit tests for the most important functions/methods/classes. Make sure that you develop these test cases to be compatible with pytest.

3. You are NOT required to submit your Git Repo for this assignment. However, I would like to strongly encourage you to keep track of your development using git with regular commits. When using Git, it is NOT good practice to have a single commit. Instead, you want to have several commits to keep track of the changes in your program and your bug fixes. 
