import socket
import http
import socketserver
import threading
import urllib
from http import server
from collections import namedtuple
from pathlib import Path
import bookmark_connection as bmc
from bookmarker import Bookmarker

BOOKMARK_PATH = "."
BOOKMARK_FILE = "pybookmark.txt"

PORT = 2024
HOST = "127.0.0.1"

class ICSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.command + " received.")
        # read post
        data = self.rfile.read(int(self.headers['content-length']))
        # decode data to str, split
        msg = data.decode(encoding = 'utf-8')
        # convert message back to python
        msg = urllib.parse.parse_qs(msg)

        # prepare response and headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        # we'll, perhaps unsafely, assume that we have a valid message if
        # data exists in pos 1 of msg parts.
        if len(msg['data'])>0:
            self.add_bookmark(msg['data'][0])
            self.wfile.write("ok".encode(encoding = 'utf-8'))
        else:
            self.wfile.write("error".encode(encoding = 'utf-8'))

    def add_bookmark(self, msg:str):
        bm = Bookmarker(p)
        bm_msg = bmc.BookmarkProtocol.open(msg)
        bm.add(bm_msg.data)
        print(f"{bm_msg.data} succesfully added")



def retrieve(_conn: bmc.Connection, bm: Bookmarker, filter: str):
    if filter == 'None':
        data = ','.join(str(n).rstrip() for n in bm.all_notes)
    else:
        data = ','.join(str(n).rstrip() for n in bm.find(filter))

    result = bmc.BookmarkProtocol(bmc.BookmarkProtocol.OK, data)
    bmc._write_command(_conn, bmc.BookmarkProtocol.format(result))

def store(_conn: bmc.Connection, bm: Bookmarker, url: str):
    '''
    store will send the command specified by the parameters
    and return a response to the command.

    url: the URL of the webpage to bookmark
    status: either 0 or 1 to indicate the status of the command
    specified in the url parameter
    '''
    try:
        bm.add(url)
        status = bmc.BookmarkProtocol(bmc.BookmarkProtocol.OK)
    except ValueError:
        status = bmc.BookmarkProtocol(bmc.BookmarkProtocol.ERROR)

    # send a response back to client to confirm receipt of message
    bmc._write_command(_conn, bmc.BookmarkProtocol.format(status))


def start_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        # instantiate the bookmark class and pass to run
        bm = Bookmarker(p)
        srv.bind((HOST, PORT))
        srv.listen()

        print("server listening on port", PORT)
        while True:
            connection, address = srv.accept()

            with connection:
                print("client connected")
                _bmc_conn = bmc.init(connection)

                while True:
                    rec_msg = bmc.listen(_bmc_conn)

                    # assume an empty message means client has disconnected
                    # so break and wait for new connection
                    if rec_msg == '': break

                    print("message: ", rec_msg)

                    try:
                        # convert message to protocol format
                        bm_msg = bmc.BookmarkProtocol.open(rec_msg)
                        # perform operation depending on protocol type
                        if bm_msg.protocol == bmc.BookmarkProtocol.ADD:
                            store(_bmc_conn, bm, bm_msg.data)
                        elif bm_msg.protocol == bmc.BookmarkProtocol.GET:
                            retrieve(_bmc_conn, bm, bm_msg.data)
                        elif bm_msg.protocol == bmc.BookmarkProtocol.DEL:
                            bm.remove_by_id(bm_msg.data)
                            bp = bmc.BookmarkProtocol(bmc.BookmarkProtocol.OK, 1)
                            bmc._write_command(_bmc_conn, bmc.BookmarkProtocol.format(bp))
                    except Exception as ex:
                        bmc.error(_bmc_conn)
                        print(ex)
                        break

                print("client disconnected")

"""
NOTE: This server is only loosely tested and therefore prone to crumbling.
If you have to restart after a crash and you receive a message that a port is
in use error, either wait about 30 seconds or just change the port here
and in client to something different, e.g., 8001
"""
def start_httpd():
    PORT = 8000
    handler = ICSHTTPRequestHandler
    httpd = socketserver.TCPServer((HOST, PORT), handler)
    print ("serving http at port", PORT)
    httpd.serve_forever()


if __name__ == '__main__':
    # the file used to store bookmarks
    p = Path(BOOKMARK_PATH) / BOOKMARK_FILE
    # if file does not exist, create it.
    if not p.exists():
        p.touch()

    """
    The following code is beyond the scope of this class, but necessary to
    run two servers at the same time. You are free to study it, but don't
    worry about what's going on too much, albeit we quickly talked about
    threading ealier during the quarter. Just know that we are using threading
    to run two processes at the same time.
    """

    threading.Thread(target=start_socket).start()
    threading.Thread(target=start_httpd).start()

