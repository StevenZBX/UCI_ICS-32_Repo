"""
Unit test for messenger module
"""

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906

import unittest
from unittest.mock import MagicMock, patch, Mock
from ds_messenger import DirectMessage, DirectMessenger


class TestDirectMessage(unittest.TestCase):
    """Unit tests for DirectMessage class."""
    def test_init(self):
        """Test initialization of DirectMessage."""
        dm = DirectMessage("msg", "to", "from", "ts")
        self.assertEqual(dm.message, "msg")
        self.assertEqual(dm.recipient, "to")
        self.assertEqual(dm.sender, "from")
        self.assertEqual(dm.timestamp, "ts")
        dm2 = DirectMessage()
        self.assertIsNone(dm2.message)


class TestDirectMessenger(unittest.TestCase):
    """Unit tests for DirectMessenger class."""
    def test_init(self):
        """Test initialization of DirectMessenger."""
        m = DirectMessenger()
        self.assertIsNone(m.token)
        with patch.object(DirectMessenger, "_connect", return_value=True), \
             patch.object(DirectMessenger, "_authenticate", return_value=True):
            m2 = DirectMessenger("server", "u", "p")
            self.assertEqual(m2.username, "u")
            self.assertEqual(m2.password, "p")
            self.assertEqual(m2.dsuserver, "server")

    def test_connect(self):
        """Test the _connect method for both success and failure."""
        m = DirectMessenger()
        with patch("socket.socket.connect"), \
             patch("socket.socket.makefile", return_value=MagicMock()):
            self.assertTrue(m._connect())
        m.sock = MagicMock()
        with patch("socket.socket.connect", side_effect=OSError("fail")):
            self.assertFalse(m._connect())

    def test_authenticate(self):
        """Test the _authenticate method for both False and True cases."""
        m = DirectMessenger("localhost", "u", "p")
        m.send_file = None
        m.recv_file = None
        self.assertFalse(m._authenticate())
        m.send_file = MagicMock()
        m.recv_file = MagicMock()
        m.send_file.write.return_value = None
        m.send_file.flush.return_value = None
        m.recv_file.readline.return_value = (
            '{"response": {"type": "ok", "token": "abc"}}\n'
        )
        self.assertTrue(m._authenticate())
        self.assertEqual(m.token, "abc")
        m.send_file.write.side_effect = OSError("fail")
        self.assertFalse(m._authenticate())

    def test_send_request(self):
        """Test the _send_request method for exception handling."""
        m = DirectMessenger("localhost", "u", "p")
        m.send_file = MagicMock()
        m.send_file.write.side_effect = OSError("fail")
        self.assertIsNone(m._send_request("req"))

    def test_send(self):
        """Test the send method for all branches."""
        m = DirectMessenger("localhost", "u", "p")
        m.token = None
        self.assertFalse(m.send("msg", "to"))
        m.token = "token"
        with patch.object(m, "_send_request", return_value=None):
            self.assertFalse(m.send("msg", "to"))
        fail_resp = Mock()
        fail_resp.type = "fail"
        with patch.object(m, "_send_request", return_value=fail_resp):
            self.assertFalse(m.send("msg", "to"))
        ok_resp = Mock()
        ok_resp.type = "ok"
        with patch.object(m, "_send_request", return_value=ok_resp):
            self.assertTrue(m.send("msg", "to"))
        with patch.object(m, "_send_request", side_effect=OSError("fail")):
            self.assertFalse(m.send("msg", "to"))

    def test_retrieve_new(self):
        """Test the retrieve_new method for all branches."""
        m = DirectMessenger("localhost", "u", "p")
        m.token = None
        self.assertFalse(m.retrieve_new())
        m.token = "token"
        with patch.object(m, "_send_request", return_value=None):
            self.assertFalse(m.retrieve_new())
        fail_resp = Mock()
        fail_resp.type = "fail"
        with patch.object(m, "_send_request", return_value=fail_resp):
            self.assertFalse(m.retrieve_new())
        ok_resp = Mock()
        ok_resp.type = "ok"
        ok_resp.messages = []
        with patch.object(m, "_send_request", return_value=ok_resp):
            self.assertFalse(m.retrieve_new())
        with patch.object(m, "_send_request", side_effect=OSError("fail")):
            self.assertFalse(m.retrieve_new())

    def test_retrieve_all(self):
        """Test the retrieve_all method for all branches."""
        m = DirectMessenger("localhost", "u", "p")
        m.token = None
        self.assertFalse(m.retrieve_all())
        m.token = "token"
        with patch.object(m, "_send_request", return_value=None):
            self.assertFalse(m.retrieve_all())
        fail_resp = Mock()
        fail_resp.type = "fail"
        with patch.object(m, "_send_request", return_value=fail_resp):
            self.assertFalse(m.retrieve_all())
        ok_resp = Mock()
        ok_resp.type = "ok"
        ok_resp.messages = []
        with patch.object(m, "_send_request", return_value=ok_resp):
            self.assertFalse(m.retrieve_all())
        with patch.object(m, "_send_request", side_effect=OSError("fail")):
            self.assertFalse(m.retrieve_all())

    def test_close(self):
        """Test the close method for all branches."""
        m = DirectMessenger()
        m.send_file = None
        m.recv_file = None
        m.sock = None
        m.close()
        m.send_file = MagicMock()
        m.recv_file = None
        m.sock = None
        m.close()
        m.send_file = None
        m.recv_file = MagicMock()
        m.sock = None
        m.close()
        m.send_file = None
        m.recv_file = None
        m.sock = MagicMock()
        m.close()

    def test_del(self):
        """Test the __del__ method for normal and exception cases."""
        m = DirectMessenger()
        m.close = MagicMock()
        del m
        m2 = DirectMessenger()

        def bad_close():
            raise OSError("fail")
        m2.close = bad_close
        try:
            del m2
        except OSError:
            self.fail("__del__ should not raise OSError")


if __name__ == "__main__":
    unittest.main()
