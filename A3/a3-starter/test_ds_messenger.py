"""
Unit test for messenger module
"""

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906


import unittest
import time

from ds_messenger import DirectMessage, DirectMessenger


class TestDSMessenger(unittest.TestCase):
    def test_direct_message_creation(self) -> None:
        """Test creating a DirectMessage object."""
        message = "Hello!"
        recipient = "user2"
        sender = "user1"
        timestamp = str(time.time())
        dm = DirectMessage(message, recipient, sender, timestamp)
        assert dm.message == message
        assert dm.recipient == recipient
        assert dm.sender == sender
        assert dm.timestamp == timestamp

    def test_direct_messenger_initialization(self) -> None:
        """Test initializing DirectMessenger with and without credentials."""
        messenger = DirectMessenger()
        assert messenger.token is None
        assert messenger.username is None
        assert messenger.password is None
        assert messenger.dsuserver == "localhost"
        assert messenger.port == 3001
        username = "testuser"
        password = "testpass"
        server = "testserver"
        messenger = DirectMessenger(server, username, password)
        assert messenger.username == username
        assert messenger.password == password
        assert messenger.dsuserver == server
        messenger.close()

    def test_send_message(self) -> None:
        """Test sending a message (requires running server)."""
        messenger = DirectMessenger(username="testuser", password="testpass")
        time.sleep(1)
        if messenger.token:
            result = messenger.send("Hello!", "recipient")
            assert isinstance(result, bool)
            messenger.close()
        else:
            messenger.close()
            self.skipTest("Server not available or authentication failed")

    def test_retrieve_messages(self) -> None:
        """Test retrieving messages (requires running server)."""
        messenger = DirectMessenger(username="testuser", password="testpass")
        time.sleep(1)
        if messenger.token:
            new_messages = messenger.retrieve_new()
            assert isinstance(new_messages, list)
            for msg in new_messages:
                assert isinstance(msg, DirectMessage)
            all_messages = messenger.retrieve_all()
            assert isinstance(all_messages, list)
            for msg in all_messages:
                assert isinstance(msg, DirectMessage)
            messenger.close()
        else:
            messenger.close()
            self.skipTest("Server not available or authentication failed")


if __name__ == "__main__":
    unittest.main() 