"""
Unit test for protocol module
"""

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906


import unittest
import json

from ds_protocol import *


class TestDSProtocol(unittest.TestCase):
    """Unit tests for the ds_protocol module."""

    def test_join_request(self) -> None:
        """Test authenticate request JSON structure."""
        username = "testuser"
        password = "testpass"
        request = authenticate(username, password)
        json_obj = json.loads(request)
        assert "authenticate" in json_obj
        assert json_obj["authenticate"]["username"] == username
        assert json_obj["authenticate"]["password"] == password

    def test_dm_request(self) -> None:
        """Test direct_message request JSON structure."""
        token = "test-token"
        message = "Hello!"
        recipient = "recipient"
        request = direct_message(token, message, recipient)
        json_obj = json.loads(request)
        assert "token" in json_obj
        assert "directmessage" in json_obj
        assert json_obj["token"] == token
        assert json_obj["directmessage"]["entry"] == message
        assert json_obj["directmessage"]["recipient"] == recipient
        assert "timestamp" in json_obj["directmessage"]

    def test_fetch_request(self) -> None:
        """Test fetch request JSON structure."""
        token = "test-token"
        status = "all"
        request = fetch(token, status)
        json_obj = json.loads(request)
        assert "token" in json_obj
        assert "fetch" in json_obj
        assert json_obj["token"] == token
        assert json_obj["fetch"] == status

    def test_auth_response(self) -> None:
        """Test extracting ServerResponse from authentication response."""
        response = '{"response": {"type": "ok", "message": "Welcome back, testuser", "token": "test-token"}}'
        result = extract_json(response)
        assert isinstance(result, ServerResponse)
        assert result.type == "ok"
        assert result.message == "Welcome back, testuser"
        assert result.token == "test-token"
        assert result.messages == []

    def test_messages_response(self) -> None:
        """Test extracting ServerResponse with messages."""
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
        assert isinstance(result.messages[0], Message)
        assert result.messages[0].message == "Hello!"
        assert result.messages[0].from_user == "user1"
        assert result.messages[0].recipient is None
        assert isinstance(result.messages[1], Message)
        assert result.messages[1].message == "Hi there!"
        assert result.messages[1].from_user is None
        assert result.messages[1].recipient == "user2"

    def test_invalid(self) -> None:
        """Test extract_json returns None for invalid JSON."""
        response = "invalid json"
        result = extract_json(response)
        assert result is None


if __name__ == "__main__":
    unittest.main() 