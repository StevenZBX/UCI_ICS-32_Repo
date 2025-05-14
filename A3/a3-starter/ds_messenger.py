# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906

import socket
import json
import time
from ds_protocol import join, direct_message, fetch, extract_json, Message

class DirectMessage:
    def __init__(self, message=None, recipient=None, sender=None, timestamp=None):
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.timestamp = timestamp

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.username = username
        self.password = password
        self.dsuserver = dsuserver or "localhost"
        self.port = 3001  # Default port as specified in the assignment
        
        # Connect and authenticate if username and password are provided
        if username and password:
            self._connect()
            self._authenticate()
    
    def _connect(self):
        """Establish connection to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.dsuserver, self.port))
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def _authenticate(self):
        """Authenticate with the server"""
        try:
            # Send join request
            join_msg = join(self.username, self.password)
            self.socket.sendall(join_msg.encode('utf-8') + b'\r\n')
            
            # Get response
            response = self.socket.recv(4096).decode('utf-8')
            result = extract_json(response)
            
            if result and result.type == "ok":
                self.token = result.token
                return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def _send_request(self, request):
        """Send a request to the server and get response"""
        try:
            self.socket.sendall(request.encode('utf-8') + b'\r\n')
            response = self.socket.recv(4096).decode('utf-8')
            return extract_json(response)
        except Exception as e:
            print(f"Failed to send request: {e}")
            return None
    
    def send(self, message: str, recipient: str) -> bool:
        """Send a direct message to a recipient"""
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
        """Retrieve new messages"""
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
        """Retrieve all messages"""
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
    
    def __del__(self):
        """Clean up socket connection when object is destroyed"""
        try:
            self.socket.close()
        except:
            pass