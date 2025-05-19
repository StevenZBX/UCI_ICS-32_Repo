import unittest
import time

from ds_messenger import DirectMessage, DirectMessenger


class TestDSMessenger(unittest.TestCase):
    def test_direct_message_creation(self):
        """Test creating a DirectMessage object."""
        message = "Hello!"
        recipient = "user2"
        sender = "user1"
        timestamp = str(time.time())
        dm = DirectMessage(message, recipient, sender, timestamp)
        self.assertEqual(dm.message, message)
        self.assertEqual(dm.recipient, recipient)
        self.assertEqual(dm.sender, sender)
        self.assertEqual(dm.timestamp, timestamp)

    def test_direct_messenger_initialization(self):
        """Test initializing DirectMessenger with and without credentials."""
        # Test without credentials
        messenger = DirectMessenger()
        self.assertIsNone(messenger.token)
        self.assertIsNone(messenger.username)
        self.assertIsNone(messenger.password)
        self.assertEqual(messenger.dsuserver, "localhost")
        self.assertEqual(messenger.port, 3001)
        # Test with credentials
        username = "testuser"
        password = "testpass"
        server = "testserver"
        messenger = DirectMessenger(server, username, password)
        self.assertEqual(messenger.username, username)
        self.assertEqual(messenger.password, password)
        self.assertEqual(messenger.dsuserver, server)
        messenger.close()

    def test_send_message(self):
        """Test sending a message (requires running server)."""
        messenger = DirectMessenger(username="testuser", password="testpass")
        time.sleep(1)
        if messenger.token:
            result = messenger.send("Hello!", "recipient")
            self.assertIsInstance(result, bool)
            messenger.close()
        else:
            messenger.close()
            self.skipTest("Server not available or authentication failed")

    def test_retrieve_messages(self):
        """Test retrieving messages (requires running server)."""
        messenger = DirectMessenger(username="testuser", password="testpass")
        time.sleep(1)
        if messenger.token:
            # Test retrieving new messages
            new_messages = messenger.retrieve_new()
            self.assertIsInstance(new_messages, list)
            for msg in new_messages:
                self.assertIsInstance(msg, DirectMessage)
            # Test retrieving all messages
            all_messages = messenger.retrieve_all()
            self.assertIsInstance(all_messages, list)
            for msg in all_messages:
                self.assertIsInstance(msg, DirectMessage)
            messenger.close()
        else:
            messenger.close()
            self.skipTest("Server not available or authentication failed")


if __name__ == "__main__":
    unittest.main() 