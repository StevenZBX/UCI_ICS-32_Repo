# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906

import socket
import json
import time

from ds_protocol import *


class DirectMessage:
    def __init__(self, message=None, recipient=None, sender=None, timestamp=None):
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.timestamp = timestamp


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initialize DirectMessenger with persistent socket connection.
        The connection is established once and reused for all requests.
        """
        self.token = None
        self.username = username
        self.password = password
        self.dsuserver = dsuserver or "localhost"
        self.port = 3001
        self.sock = None
        self.send_file = None
        self.recv_file = None
        if username and password:
            self._connect()
            self._authenticate()

    def _connect(self):
        """Establish a persistent socket connection to the server."""
        try:
            if self.sock:
                self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.dsuserver, self.port))
            self.send_file = self.sock.makefile('w')
            self.recv_file = self.sock.makefile('r')
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.sock = None
            self.send_file = None
            self.recv_file = None
            return False

    def _authenticate(self):
        """Authenticate with the server using the persistent connection."""
        try:
            msg = authenticate(self.username, self.password)
            self.send_file.write(msg + '\r\n')
            self.send_file.flush()
            response = self.recv_file.readline()
            result = extract_json(response)
            if result and result.type == "ok":
                self.token = result.token
                return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def _send_request(self, request):
        """Send a request to the server and get response using the persistent connection."""
        try:
            self.send_file.write(request + '\r\n')
            self.send_file.flush()
            response = self.recv_file.readline()
            return extract_json(response)
        except Exception as e:
            print(f"Failed to send request: {e}")
            return None

    def send(self, message: str, recipient: str) -> bool:
        """Send a direct message to a recipient using the persistent connection."""
        if not self.token:
            return False
        try:
            request = direct_message(self.token, message, recipient)
            result = self._send_request(request)
            return result and result.type == "ok"
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False

    def retrieve_new(self) -> list:
        """Retrieve new messages using the persistent connection."""
        if not self.token:
            return []
        try:
            request = fetch(self.token, "unread")
            result = self._send_request(request)
            if result and result.type == "ok":
                messages = []
                for msg in result.messages:
                    dm = DirectMessage(
                        message=msg.message,
                        sender=msg.from_user,
                        timestamp=msg.timestamp
                    )
                    messages.append(dm)
                return messages
            return []
        except Exception as e:
            print(f"Failed to retrieve new messages: {e}")
            return []

    def retrieve_all(self) -> list:
        """Retrieve all messages using the persistent connection."""
        if not self.token:
            return []
        try:
            request = fetch(self.token, "all")
            result = self._send_request(request)
            if result and result.type == "ok":
                messages = []
                for msg in result.messages:
                    dm = DirectMessage(
                        message=msg.message,
                        sender=msg.from_user,
                        recipient=msg.recipient,
                        timestamp=msg.timestamp
                    )
                    messages.append(dm)
                return messages
            return []
        except Exception as e:
            print(f"Failed to retrieve all messages: {e}")
            return []

    def close(self):
        """Close the persistent socket connection and associated files."""
        try:
            if self.send_file:
                self.send_file.close()
            if self.recv_file:
                self.recv_file.close()
            if self.sock:
                self.sock.close()
        except Exception:
            pass

    def __del__(self):
        """Ensure the socket connection is closed when the object is destroyed."""
        self.close()