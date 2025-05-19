# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906

import json
from collections import namedtuple
import time


# Create namedtuples to hold the values we expect to retrieve from json messages
Message = namedtuple('Message', ['message', 'from_user', 'timestamp', 'recipient'])
ServerResponse = namedtuple('ServerResponse', ['type', 'message', 'token', 'messages'])


def authenticate(username: str, password: str) -> str:
    """
    Create an authenticate request message
    """
    return json.dumps({
        "authenticate": {
            "username": username,
            "password": password
        }
    })


def direct_message(token: str, message: str, recipient: str) -> str:
    """
    Create a direct message request
    """
    return json.dumps({
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": str(time.time())
        }
    })


def fetch(token: str, status: str) -> str:
    """
    Create a fetch request for messages
    status can be either "all" or "unread"
    """
    return json.dumps({
        "token": token,
        "fetch": status
    })


def extract_json(json_msg: str) -> ServerResponse:
    """
    Parse a JSON response from the server into a ServerResponse namedtuple
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        
        # Extract basic response fields
        type_val = response.get('type')
        message = response.get('message')
        token = response.get('token')
        
        # Extract messages if they exist
        messages = []
        if 'messages' in response:
            for msg in response['messages']:
                # Handle both incoming and outgoing messages
                if 'from' in msg:
                    messages.append(Message(
                        message=msg['message'],
                        from_user=msg['from'],
                        timestamp=msg['timestamp'],
                        recipient=None
                    ))
                elif 'recipient' in msg:
                    messages.append(Message(
                        message=msg['message'],
                        from_user=None,
                        timestamp=msg['timestamp'],
                        recipient=msg['recipient']
                    ))
        
        return ServerResponse(type_val, message, token, messages)
        
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None
    except KeyError as e:
        print(f"Missing key in JSON response: {e}")
        return None
