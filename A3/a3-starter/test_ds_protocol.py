import pytest
from ds_protocol import join, direct_message, fetch, extract_json, ServerResponse, Message

def test_join_request():
    """Test creating a join request"""
    username = "testuser"
    password = "testpass"
    request = join(username, password)
    
    # Verify the request is valid JSON
    import json
    json_obj = json.loads(request)
    
    assert "join" in json_obj
    assert json_obj["join"]["username"] == username
    assert json_obj["join"]["password"] == password

def test_direct_message_request():
    """Test creating a direct message request"""
    token = "test-token"
    message = "Hello!"
    recipient = "recipient"
    request = direct_message(token, message, recipient)
    
    # Verify the request is valid JSON
    import json
    json_obj = json.loads(request)
    
    assert "token" in json_obj
    assert "directmessage" in json_obj
    assert json_obj["token"] == token
    assert json_obj["directmessage"]["entry"] == message
    assert json_obj["directmessage"]["recipient"] == recipient
    assert "timestamp" in json_obj["directmessage"]

def test_fetch_request():
    """Test creating a fetch request"""
    token = "test-token"
    what = "all"
    request = fetch(token, what)
    
    # Verify the request is valid JSON
    import json
    json_obj = json.loads(request)
    
    assert "token" in json_obj
    assert "fetch" in json_obj
    assert json_obj["token"] == token
    assert json_obj["fetch"] == what

def test_extract_json_auth_response():
    """Test parsing an authentication response"""
    response = '{"response": {"type": "ok", "message": "Welcome back, testuser", "token": "test-token"}}'
    result = extract_json(response)
    
    assert isinstance(result, ServerResponse)
    assert result.type == "ok"
    assert result.message == "Welcome back, testuser"
    assert result.token == "test-token"
    assert result.messages == []

def test_extract_json_messages_response():
    """Test parsing a messages response"""
    response = '''{
        "response": {
            "type": "ok",
            "messages": [
                {
                    "message": "Hello!",
                    "from": "user1",
                    "timestamp": "1603167689.3928561"
                },
                {
                    "message": "Hi there!",
                    "recipient": "user2",
                    "timestamp": "1603167699.3928561"
                }
            ]
        }
    }'''
    result = extract_json(response)
    
    assert isinstance(result, ServerResponse)
    assert result.type == "ok"
    assert len(result.messages) == 2
    
    # Check first message (incoming)
    assert isinstance(result.messages[0], Message)
    assert result.messages[0].message == "Hello!"
    assert result.messages[0].from_user == "user1"
    assert result.messages[0].recipient is None
    
    # Check second message (outgoing)
    assert isinstance(result.messages[1], Message)
    assert result.messages[1].message == "Hi there!"
    assert result.messages[1].from_user is None
    assert result.messages[1].recipient == "user2"

def test_extract_json_invalid():
    """Test parsing invalid JSON"""
    response = "invalid json"
    result = extract_json(response)
    assert result is None 