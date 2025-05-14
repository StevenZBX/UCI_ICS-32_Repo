import pytest
from ds_messenger import DirectMessage, DirectMessenger
import time

def test_direct_message_creation():
    """Test creating a DirectMessage object"""
    message = "Hello!"
    recipient = "user2"
    sender = "user1"
    timestamp = str(time.time())
    
    dm = DirectMessage(message, recipient, sender, timestamp)
    
    assert dm.message == message
    assert dm.recipient == recipient
    assert dm.sender == sender
    assert dm.timestamp == timestamp

def test_direct_messenger_initialization():
    """Test initializing DirectMessenger with and without credentials"""
    # Test without credentials
    messenger = DirectMessenger()
    assert messenger.token is None
    assert messenger.username is None
    assert messenger.password is None
    assert messenger.dsuserver == "localhost"
    assert messenger.port == 3001
    
    # Test with credentials
    username = "testuser"
    password = "testpass"
    server = "testserver"
    messenger = DirectMessenger(server, username, password)
    assert messenger.username == username
    assert messenger.password == password
    assert messenger.dsuserver == server

def test_send_message():
    """Test sending a message"""
    # Note: This test requires a running server
    messenger = DirectMessenger(username="testuser", password="testpass")
    
    # Wait for authentication
    time.sleep(1)
    
    if messenger.token:
        result = messenger.send("Hello!", "recipient")
        assert isinstance(result, bool)
    else:
        pytest.skip("Server not available or authentication failed")

def test_retrieve_messages():
    """Test retrieving messages"""
    # Note: This test requires a running server
    messenger = DirectMessenger(username="testuser", password="testpass")
    
    # Wait for authentication
    time.sleep(1)
    
    if messenger.token:
        # Test retrieving new messages
        new_messages = messenger.retrieve_new()
        assert isinstance(new_messages, list)
        for msg in new_messages:
            assert isinstance(msg, DirectMessage)
        
        # Test retrieving all messages
        all_messages = messenger.retrieve_all()
        assert isinstance(all_messages, list)
        for msg in all_messages:
            assert isinstance(msg, DirectMessage)
    else:
        pytest.skip("Server not available or authentication failed") 