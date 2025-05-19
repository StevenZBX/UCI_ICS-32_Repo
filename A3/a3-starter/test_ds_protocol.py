import unittest
import json

from ds_protocol import *


class TestDSProtocol(unittest.TestCase):
    def test_authenticate_request(self):
        username = "testuser"
        password = "testpass"
        request = authenticate(username, password)
        json_obj = json.loads(request)
        self.assertIn("authenticate", json_obj)
        self.assertEqual(json_obj["authenticate"]["username"], username)
        self.assertEqual(json_obj["authenticate"]["password"], password)

    def test_direct_message_request(self):
        token = "test-token"
        message = "Hello!"
        recipient = "recipient"
        request = direct_message(token, message, recipient)
        json_obj = json.loads(request)
        self.assertIn("token", json_obj)
        self.assertIn("directmessage", json_obj)
        self.assertEqual(json_obj["token"], token)
        self.assertEqual(json_obj["directmessage"]["entry"], message)
        self.assertEqual(json_obj["directmessage"]["recipient"], recipient)
        self.assertIn("timestamp", json_obj["directmessage"])

    def test_fetch_request(self):
        token = "test-token"
        what = "all"
        request = fetch(token, what)
        json_obj = json.loads(request)
        self.assertIn("token", json_obj)
        self.assertIn("fetch", json_obj)
        self.assertEqual(json_obj["token"], token)
        self.assertEqual(json_obj["fetch"], what)

    def test_extract_json_auth_response(self):
        response = '{"response": {"type": "ok", "message": "Welcome back, testuser", "token": "test-token"}}'
        result = extract_json(response)
        self.assertIsInstance(result, ServerResponse)
        self.assertEqual(result.type, "ok")
        self.assertEqual(result.message, "Welcome back, testuser")
        self.assertEqual(result.token, "test-token")
        self.assertEqual(result.messages, [])

    def test_extract_json_messages_response(self):
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
        self.assertIsInstance(result, ServerResponse)
        self.assertEqual(result.type, "ok")
        self.assertEqual(len(result.messages), 2)
        self.assertIsInstance(result.messages[0], Message)
        self.assertEqual(result.messages[0].message, "Hello!")
        self.assertEqual(result.messages[0].from_user, "user1")
        self.assertIsNone(result.messages[0].recipient)
        self.assertIsInstance(result.messages[1], Message)
        self.assertEqual(result.messages[1].message, "Hi there!")
        self.assertIsNone(result.messages[1].from_user)
        self.assertEqual(result.messages[1].recipient, "user2")

    def test_extract_json_invalid(self):
        response = "invalid json"
        result = extract_json(response)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main() 