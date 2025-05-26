"""
Unit test for messenger module
"""

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906


import unittest
import time
from unittest.mock import MagicMock, patch

from ds_messenger import DirectMessage, DirectMessenger


class TestDSMessenger(unittest.TestCase):
    """Unit tests for the DirectMessenger and DirectMessage classes."""

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

    def test_send_token_none(self) -> None:
        """Test send returns False when token is None."""
        messenger = DirectMessenger()
        assert messenger.send("msg", "to") is False

    def test_retrieve_new_token_none(self) -> None:
        """Test retrieve_new returns [] when token is None."""
        messenger = DirectMessenger()
        assert messenger.retrieve_new() == []

    def test_retrieve_all_token_none(self) -> None:
        """Test retrieve_all returns [] when token is None."""
        messenger = DirectMessenger()
        assert messenger.retrieve_all() == []

    def test_connect_exception(self) -> None:
        """Test _connect handles exceptions and resets attributes."""
        messenger = DirectMessenger()
        with patch("socket.socket.connect", side_effect=OSError("fail")):
            assert messenger._connect() is False

    def test_authenticate_exception(self) -> None:
        """Test _authenticate handles exceptions and prints error."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.send_file = MagicMock()
        messenger.recv_file = MagicMock()
        messenger.send_file.write.side_effect = OSError("fail")
        assert messenger._authenticate() is False

    def test_send_request_exception(self) -> None:
        """Test _send_request handles exceptions and prints error."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.send_file = MagicMock()
        messenger.send_file.write.side_effect = OSError("fail")
        assert messenger._send_request("req") is None

    def test_send_exception(self) -> None:
        """Test send handles exceptions and prints error."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.token = "token"
        with patch.object(messenger, "_send_request", side_effect=OSError("fail")):
            assert messenger.send("msg", "to") is False

    def test_retrieve_new_exception(self) -> None:
        """Test retrieve_new handles exceptions and prints error."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.token = "token"
        with patch.object(messenger, "_send_request", side_effect=OSError("fail")):
            assert messenger.retrieve_new() == []

    def test_retrieve_all_exception(self) -> None:
        """Test retrieve_all handles exceptions and prints error."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.token = "token"
        with patch.object(messenger, "_send_request", side_effect=OSError("fail")):
            assert messenger.retrieve_all() == []

    def test_close_all_none(self) -> None:
        """Test close when all file/socket attributes are None."""
        messenger = DirectMessenger()
        messenger.send_file = None
        messenger.recv_file = None
        messenger.sock = None
        messenger.close()  # Should not raise

    def test_close_with_files(self) -> None:
        """Test close when file/socket attributes are present."""
        messenger = DirectMessenger()
        messenger.send_file = MagicMock()
        messenger.recv_file = MagicMock()
        messenger.sock = MagicMock()
        messenger.close()  # Should call close on all

    def test_del_calls_close(self) -> None:
        """Test __del__ calls close method."""
        messenger = DirectMessenger()
        messenger.close = MagicMock()
        del messenger  # Should call close

    def test_connect_print_and_reset(self) -> None:
        """Test _connect prints error and resets attributes on exception."""
        messenger = DirectMessenger()
        with patch("socket.socket.connect", side_effect=OSError("fail")):
            messenger.sock = None
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            result = messenger._connect()
            sys.stdout = old_stdout
        assert "Failed to connect to server" in mystdout.getvalue()
        assert result is False
        assert messenger.sock is None
        assert messenger.send_file is None
        assert messenger.recv_file is None

    def test_authenticate_print(self) -> None:
        """Test _authenticate prints error on exception."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.send_file = MagicMock()
        messenger.recv_file = MagicMock()
        messenger.send_file.write.side_effect = OSError("fail")
        import sys
        from io import StringIO
        captured = StringIO()
        sys.stdout = captured
        result = messenger._authenticate()
        sys.stdout = sys.__stdout__
        assert "Authentication failed" in captured.getvalue()
        assert result is False

    def test_send_request_print(self) -> None:
        """Test _send_request prints error on exception."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.send_file = MagicMock()
        messenger.send_file.write.side_effect = OSError("fail")
        import sys
        from io import StringIO
        captured = StringIO()
        sys.stdout = captured
        result = messenger._send_request("req")
        sys.stdout = sys.__stdout__
        assert "Failed to send request" in captured.getvalue()
        assert result is None

    def test_send_print(self) -> None:
        """Test send prints error on exception."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.token = "token"
        with patch.object(messenger, "_send_request", side_effect=OSError("fail")):
            import sys
            from io import StringIO
            captured = StringIO()
            sys.stdout = captured
            result = messenger.send("msg", "to")
            sys.stdout = sys.__stdout__
            assert "Failed to send message" in captured.getvalue()
            assert result is False

    def test_retrieve_new_print(self) -> None:
        """Test retrieve_new prints error on exception."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.token = "token"
        with patch.object(messenger, "_send_request", side_effect=OSError("fail")):
            import sys
            from io import StringIO
            captured = StringIO()
            sys.stdout = captured
            result = messenger.retrieve_new()
            sys.stdout = sys.__stdout__
            assert "Failed to retrieve new messages" in captured.getvalue()
            assert result == []

    def test_retrieve_all_print(self) -> None:
        """Test retrieve_all prints error on exception."""
        messenger = DirectMessenger("localhost", "u", "p")
        messenger.token = "token"
        with patch.object(messenger, "_send_request", side_effect=OSError("fail")):
            import sys
            from io import StringIO
            captured = StringIO()
            sys.stdout = captured
            result = messenger.retrieve_all()
            sys.stdout = sys.__stdout__
            assert "Failed to retrieve all messages" in captured.getvalue()
            assert result == []

    def test_close_exception(self) -> None:
        """Test close handles exceptions when closing files or sockets."""
        messenger = DirectMessenger()
        class Dummy:
            def close(self): raise OSError("fail")
        messenger.send_file = Dummy()
        messenger.recv_file = Dummy()
        messenger.sock = Dummy()
        # Should not raise
        messenger.close()

    def test_del_calls_close_final(self) -> None:
        """Test __del__ calls close method。"""
        messenger = DirectMessenger()
        messenger.close = MagicMock()
        messenger.__del__()
        messenger.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
