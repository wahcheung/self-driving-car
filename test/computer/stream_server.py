# -*- coding: utf-8 -*-

import cv2
import io
import numpy as np
import os
import socket
import struct
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../")
from config.settings import *


class VideoStreamingServer(object):
    def __init__(self, host, port):
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        # Accept a single connection and make a file-like object out of it
        self.connection = self.server_socket.accept()[0].makefile('rb')
        print("Streaming Socket Connected!")

    def streaming(self):
        try:
            count = 0
            while True:
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
                # Rewind the stream
                image_stream.seek(0)
                img = image_stream.read()
                img_array = np.frombuffer(img, dtype=np.uint8)
                cv_image = cv2.imdecode(img_array, 1)
                image_name = "IMG_%s" % count
                cv2.imshow(image_name, cv_image)
                cv2.waitKey(500)
                cv2.destroyWindow(image_name)
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == "__main__":
    server = VideoStreamingServer(SERVER_HOST, VIDEO_STREAMING_PORT)
    server.streaming()
