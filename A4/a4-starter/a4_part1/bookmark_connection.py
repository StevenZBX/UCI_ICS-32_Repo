# bookmark_connection.py
#
# ICS 32 Lab
# Code Example
#
# This is a helper module that provides functions
# common to both client and server.
# So type annotations in python 3.10 and below are not capable of interpreting
# type hints of methods that have parameters as the same type as
# the enclosing class. The following import gets us around that.
# If you are using some IDE, feel free to comment out to see
# the difference if you are in PyCharm or VS Code
from __future__ import annotations

import enum
import socket
from collections import namedtuple

class BookmarkServerError(Exception):
    pass

"""
A namedtuple conveniently encapsulates the objects we need to use to
communicate over a socket connection in many of the functions in this module.
Rather than pass multiple objects, it is cleaner to wrap them in a namedtuple.
"""
Connection = namedtuple('Connection',['socket','send','recv'])

"""
A simple protocol for managing communication between
PyBookmark Online servers and clients
"""
class BookmarkProtocol:
    # known protocol command types (only three for now!)
    ERROR = "0"
    OK = "1"
    ADD = "2"
    GET = "3"
    DEL = "4"

    def __init__(self, protocol=None, data=None) -> None:
        self.protocol = protocol
        self.data = data

    # Note that these are both static methods, called without instantiation
    def format(bp: BookmarkProtocol) -> str:
        """
        formats a protocol command type and message into a
        format that both client and server
        can understand
        """
        return f"{bp.protocol}|{bp.data}"

    def open(cmd: str) -> BookmarkProtocol:
        """
        extracts a protocol command type and message
        into a BookmarkProtocol object
        """
        parts = cmd.split("|")
        if len(parts) > 1:
            return BookmarkProtocol(parts[0], parts[1])
        else:
            # something is wrong with the cmd, so convert to error.
            return BookmarkProtocol(BookmarkProtocol.ERROR)

"""
Place new functions that extend the functionality of the
PyBookmark Online platform here.
"""
def add(_conn: Connection, url: str) -> BookmarkProtocol:
    '''
    add will send the command specified by the parameters
    and return a response to the command.

    url: the URL of the webpage to bookmark
    '''
    # prepare message using Bookmark Protocol format
    bm = BookmarkProtocol(BookmarkProtocol.ADD, url)
    cmd = BookmarkProtocol.format(bm)
    _write_command(_conn, cmd)
    return BookmarkProtocol.open(_read_command(_conn))

# TODO: Add functions to support new features here
def get(_conn: Connection, param: any) -> list:
    bm = BookmarkProtocol(BookmarkProtocol.GET)
    cmd = BookmarkProtocol.format(bm)
    _write_command(_conn, cmd)
    return BookmarkProtocol.open(_read_command(_conn))

def delete(_conn: Connection, index: int) -> bool:
    bm = BookmarkProtocol(BookmarkProtocol.DEL, index)
    cmd = BookmarkProtocol.format(bm)
    _write_command(_conn, cmd)
    return BookmarkProtocol.open(_read_command(_conn))



"""
The following functions are useful for handling socket connections
"""
def init(sock: socket) -> Connection:
    '''
    The init method should be called for every program that uses this module.
    The calling program should first establish a connection with a socket
    object, then pass that open socket to init.
    init will then create file objects to handle input and output.
    '''
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
    except:
        raise BookmarkServerError("Invalid socket connection")

    return Connection(
        socket = sock,
        send = f_send,
        recv = f_recv
    )

def disconnect(_conn: Connection):
    '''
    provide a way to close read and write file objects
    '''
    _conn.send.close()
    _conn.recv.close()

def listen(_conn: Connection) -> str:
    '''
    listen will block until a new message has been received
    '''
    return _read_command(_conn)

def error(_conn: Connection):
    '''
    a send only wrapper that sends 0 for an error
    '''
    _write_command(_conn, str(0))

def complete(_conn: Connection):
    '''
    a send only wrapper that sends 1 for complete success
    '''
    _write_command(_conn, str(1))

def _write_command(_conn: Connection, cmd: str):
    '''
    performs the required steps to send a message,
    including appending a newline sequence and flushing the socket to ensure
    the message is sent immediately.
    '''
    try:
        _conn.send.write(cmd + '\n')
        _conn.send.flush()
    except:
        raise BookmarkServerError

def _read_command(_conn: Connection) -> str:
    '''
    performs the required steps to receive a message. Trims the
    newline sequence before returning
    '''
    cmd = _conn.recv.readline()[:-1]
    return cmd
