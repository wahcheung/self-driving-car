# -*- coding: utf-8 -*-

import io
import os
import picamera
import socket
import struct
import sys
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../")
from config.settings import *


class VideoStreamingClient(object):
    def __init__(self, host, port):
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))
        # Make a file-like object out of the connection
        self.connection = self.client_socket.makefile('wb')
        print("Streaming Socket Connected!")

    def streaming(self):
        count = 0
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = RESOLUTION
                # Start a preview and let the camera warm up for 2 seconds
                camera.start_preview()
                time.sleep(2)

                stream = io.BytesIO()
                for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                    # Write the length of the capture to the stream and flush to ensure it actually gets sent
                    # '<L' 表示使用小端模式写入Unsigned Long类型, 此处写入的是图像的字节流长度
                    self.connection.write(struct.pack('<L', stream.tell()))
                    self.connection.flush()
                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    self.connection.write(stream.read())
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
                    count += 1
                    print("Streaming count: %s" % count)
        except KeyboardInterrupt:
            # Write a length of zero to the stream to signal we're done
            self.connection.write(struct.pack('<L', 0))
        finally:
            self.connection.close()
            self.client_socket.close()


if __name__ == "__main__":
    client = VideoStreamingClient(host=COMPUTER_HOST, port=VIDEO_STREAMING_PORT)
    client.streaming()
