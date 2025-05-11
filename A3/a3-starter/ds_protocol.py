# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

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
