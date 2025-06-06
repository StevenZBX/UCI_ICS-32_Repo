# NAME Boxuan Zhang
# EMAIL boxuanz3@uci.edu
# STUDENT ID 95535906

import urllib.request
import bookmark_connection as bmc
from bookmark_connection import BookmarkProtocol

"""
The following code snippets can be used to help you prepare your test function:
The url to use for testing.
Be sure to run bookmark_server.py before making requests!

url = 'http://localhost:8000'

The format to use for your request data.
Don't forget to encode before sending a request!

json = {'data':bmc.BookmarkProtocol.format(
                                BookmarkProtocol(BookmarkProtocol.ADD, data))}
"""

def http_api_test(url, data):
    # TODO: write your http connection code here. You can use the above snippets to help
    json = {'data':bmc.BookmarkProtocol.format(
                                BookmarkProtocol(BookmarkProtocol.ADD, data))}
    test_data = urllib.parse.urlencode(json)
    test_data = test_data.encode('utf-8')
    header = {"content-type": "application/json"}
    req = urllib.request.Request(url, test_data, header)

    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        return response.read().decode()


if __name__ == '__main__':
    # TODO: call your test code from here. You might try writing a few different url tests.
    url = 'http://localhost:8000'
    assert http_api_test(url, "https://example.com") == "ok"
    assert http_api_test(url, "https://111.com") == "ok"
    assert http_api_test(url, "https://test.com") == "ok"
    assert http_api_test(url, "123") == ""