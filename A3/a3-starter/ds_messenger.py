"""
Module for managing sending messages and receiving messages
"""

# ds_messenger.py


# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906


import socket
import json

from ds_protocol import authenticate, extract_json
from ds_protocol import direct_message, fetch, ServerResponse


class DirectMessage:
    """
    Class for message detail of content, sender, time and recipient
    """
    def __init__(self, message=None, recipient=None,
                 sender=None, timestamp=None) -> None:
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.timestamp = timestamp


class DirectMessenger:
    """
    Class for authenticating, sending, fetching messages
    """
    def __init__(self, dsuserver=None, username=None, password=None) -> None:
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

    def _connect(self) -> bool:
        """Establish a persistent socket connection to the server."""
        try:
            if self.sock:
                self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.dsuserver, self.port))
            self.send_file = self.sock.makefile('w')
            self.recv_file = self.sock.makefile('r')
            return True
        except (OSError, ValueError, socket.error) as e:
            print(f"Failed to connect to server: {e}")
            self.sock = None
            self.send_file = None
            self.recv_file = None
            return False

    def _authenticate(self) -> bool:
        """Authenticate with the server using the persistent connection."""
        try:
            if self.send_file is None or self.recv_file is None:
                return False
            msg = authenticate(self.username, self.password)
            self.send_file.write(msg + '\r\n')
            self.send_file.flush()
            response = self.recv_file.readline()
            result = extract_json(response)
            if result and result.type == "ok":
                self.token = result.token
                return True
            return False
        except (OSError, ValueError, socket.error, json.JSONDecodeError) as e:
            print(f"Authentication failed: {e}")
            return False

    def _send_request(self, request: str) -> None or ServerResponse:
        """
        Send a request to the server
        and get response using the persistent connection.
        """
        try:
            self.send_file.write(request + '\r\n')
            self.send_file.flush()
            response = self.recv_file.readline()
            return extract_json(response)
        except (OSError, ValueError, socket.error, json.JSONDecodeError) as e:
            print(f"Failed to send request: {e}")
            return None

    def send(self, message: str, recipient: str) -> bool:
        """
        Send a direct message to a recipient
        using the persistent connection.
        """
        if not self.token:
            return False
        try:
            request = direct_message(self.token, message, recipient)
            result = self._send_request(request)
            return result and result.type == "ok"
        except (OSError, ValueError, socket.error, json.JSONDecodeError) as e:
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
        except (OSError, ValueError, socket.error, json.JSONDecodeError) as e:
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
        except (OSError, ValueError, socket.error, json.JSONDecodeError) as e:
            print(f"Failed to retrieve all messages: {e}")
            return []

    def close(self) -> None:
        """Close the persistent socket connection and associated files."""
        try:
            if self.send_file:
                self.send_file.close()
            if self.recv_file:
                self.recv_file.close()
            if self.sock:
                self.sock.close()
        except (OSError, ValueError, socket.error):
            pass

    def __del__(self) -> None:
        """
        Ensure the socket connection is closed when the object is destroyed.
        """
        try:
            self.close()
        except (OSError, ValueError, socket.error):
            pass
