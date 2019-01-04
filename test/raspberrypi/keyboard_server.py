# -*- coding: utf-8 -*-

import os
import socket
import struct
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../")
from config.settings import *


class KeyboardServer(object):
    def __init__(self, host, port):
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection = self.server_socket.accept()[0]
        print("Keyboard Socket Connected!")

    def receive(self):
        code2str = {
            STOP:               "Stop",
            LEFT:               "Left",
            RIGHT:              "Right",
            FORWARD:            "Forward",
            FORWARD | LEFT:     "Forward Left",
            FORWARD | RIGHT:    "Forward Right",
            BACKWARD:           "Backward",
            BACKWARD | LEFT:    "Backward Left",
            BACKWARD | RIGHT:   "Backward Right",
            SHUTDOWN:           "Shutdown"
        }
        while True:
            op = struct.unpack('<I', self.connection.recv(struct.calcsize('<I')))[0]
            print("Receive: %s" % code2str[op])
            if op == SHUTDOWN:
                self.connection.close()
                print("Connection Closed!")
                sys.exit(0)


if __name__ == "__main__":
    server = KeyboardServer(host=SERVER_HOST, port=KEYBOARD_PORT)
    server.receive()
