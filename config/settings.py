# -*- coding: utf-8 -*-

# 直流电机连接的树莓派引脚(BCM编号)
LEFT_PIN_A = 6
LEFT_PIN_B = 5
LEFT_PWM = 0
RIGHT_PIN_A = 22
RIGHT_PIN_B = 27
RIGHT_PWM = 17

# 小车5档调速
GEARS = [0, 1, 2, 3, 4]

# 定义操作指令, 小车有可以执行下面几种命令并且可以是某些命令的组合
STOP     = 0x0000
LEFT     = 0x0001
RIGHT    = 0x0010
FORWARD  = 0x0100
BACKWARD = 0x1000
SHUTDOWN = 0x1111

SERVER_HOST = "0.0.0.0"
PI_HOST = "192.168.0.7"
COMPUTER_HOST = "192.168.0.246"
VIDEO_STREAMING_PORT = 8000
KEYBOARD_PORT = 8001

# 设定摄像头拍摄的图像大小
RESOLUTION = (640, 480)
