

import socket
import sys
import threading
import traceback

import paramiko







host_key = paramiko.RSAKey(filename="test_rsa.key")


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "root") and (password == "toor"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

try:
        global sock
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(('10.0.2.15',22))
        sock.listen(1)
        print ('Listening for connection...')

except Exception as e:
        print('Error' + str(e))

try:
    client, addr = sock.accept()
    print('Got a connection from ' + str(addr))
    t = paramiko.Transport(client)
    t.load_server_module()
    t.add_server_key(host_key)
    server = Server()
    t.start_server(server=server)
    global chan
    chan = t.accept(1)
    print (chan.recv(1024))
    chan.send('lol')

except Exception as e:
    print ('Connection terminated \n' + str(e))
    pass

