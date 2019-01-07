# -*- coding: utf-8 -*-

import os
import pygame
import socket
import struct
import sys
from pygame.locals import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../")
from config.settings import *


class KeyboardClient(object):
    def __init__(self, host, port):
        pygame.init()
        pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Pygame Keyboard Monitoring')
        # 键盘指令客户端(client), 将键盘输入的指令发送到树莓派
        self.keyboard_client_socket = socket.socket()
        self.keyboard_client_socket.connect((host, port))
        print("Keyboard Socket Connected!")

    def monitor(self):
        """监控键盘事件并通知服务端"""
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        key = pygame.key.get_pressed()
                        if key[pygame.K_UP] and key[pygame.K_LEFT]:
                            print("Forward Left")
                            self.keyboard_client_socket.send(struct.pack('<I', FORWARD | LEFT))
                        elif key[pygame.K_UP] and key[pygame.K_RIGHT]:
                            print("Forward Right")
                            self.keyboard_client_socket.send(struct.pack('<I', FORWARD | RIGHT))
                        elif key[pygame.K_DOWN] and key[pygame.K_LEFT]:
                            print("Backward Left")
                            self.keyboard_client_socket.send(struct.pack('<I', BACKWARD | LEFT))
                        elif key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
                            print("Backward Right")
                            self.keyboard_client_socket.send(struct.pack('<I', BACKWARD | RIGHT))
                        elif key[pygame.K_LEFT]:
                            print("Left")
                            self.keyboard_client_socket.send(struct.pack('<I', LEFT))
                        elif key[pygame.K_RIGHT]:
                            print("Right")
                            self.keyboard_client_socket.send(struct.pack('<I', RIGHT))
                        elif key[pygame.K_UP]:
                            print("Forward")
                            self.keyboard_client_socket.send(struct.pack('<I', FORWARD))
                        elif key[pygame.K_DOWN]:
                            print("Backward")
                            self.keyboard_client_socket.send(struct.pack('<I', BACKWARD))
                        elif key[K_ESCAPE]:
                            print("Shutdown and Exit")
                            self.keyboard_client_socket.send(struct.pack('<I', STOP))
                            self.keyboard_client_socket.send(struct.pack('<I', SHUTDOWN))
                            sys.exit(0)
                        else:
                            print("Undefined Option")
                    elif event.type == pygame.KEYUP:
                        print("Stop")
                        self.keyboard_client_socket.send(struct.pack('<I', STOP))

        finally:
            print("Connection Closed!")
            self.keyboard_client_socket.close()


if __name__ == "__main__":
    keyboard = KeyboardClient(host=PI_HOST, port=KEYBOARD_PORT)
    keyboard.monitor()
