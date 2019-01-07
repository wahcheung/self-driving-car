# -*- coding: utf-8 -*-

import os
import RPi.GPIO as GPIO
import socket
import struct
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../")
from config.settings import *


class Wheel(object):
    def __init__(self, pin_e, pin_a, pin_b):
        """
        :param pin_e: 电机控制信号使能端口
        :param pin_a: 电机控制信号端口之一
        :param pin_b: 电机控制信号端口之二
        """
        self.PIN_E = pin_e
        self.PIN_A = pin_a
        self.PIN_B = pin_b
        GPIO.setup(self.PIN_E, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PIN_A, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PIN_B, GPIO.OUT, initial=GPIO.LOW)
        # PWM频率初始化为100Hz, 占空比(Duty Cycle)初始化为100%
        self.pwm = GPIO.PWM(self.PIN_E, 100)
        self.pwm.start(100)
        # 小车速度档位
        self.gear = 0

    def forward(self):
        """正转"""
        GPIO.output(self.PIN_A, GPIO.HIGH)
        GPIO.output(self.PIN_B, GPIO.LOW)

    def backward(self):
        """反转"""
        GPIO.output(self.PIN_A, GPIO.LOW)
        GPIO.output(self.PIN_B, GPIO.HIGH)

    def speed_up(self):
        """加速"""
        if self.gear < len(GEARS) - 1:
            self.gear += 1
            self.pwm.ChangeDutyCycle(100 * self.gear / (len(GEARS) - 1))

    def slow_down(self):
        """减速"""
        if self.gear > 0:
            self.gear -= 1
            self.pwm.ChangeDutyCycle(100 * self.gear / (len(GEARS) - 1))

    def stop(self):
        """制动"""
        GPIO.output(self.PIN_A, GPIO.LOW)
        GPIO.output(self.PIN_B, GPIO.LOW)


class Car(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.left_wheel = Wheel(LEFT_PWM, LEFT_PIN_A, LEFT_PIN_B)
        self.right_wheel = Wheel(RIGHT_PWM, RIGHT_PIN_A, RIGHT_PIN_B)
        self.direction = FORWARD
        print("Car is ready!")

    def forward(self):
        """前进档"""
        self.direction = FORWARD
        self.left_wheel.forward()
        self.right_wheel.forward()

    def backward(self):
        """倒车档"""
        self.direction = BACKWARD
        self.left_wheel.backward()
        self.right_wheel.backward()

    def speed_up(self):
        """加速"""
        self.left_wheel.speed_up()
        self.right_wheel.speed_up()

    def slow_down(self):
        """减速"""
        self.left_wheel.slow_down()
        self.right_wheel.slow_down()

    def turn_left(self):
        """左转"""
        self.left_wheel.stop()
        if self.direction == FORWARD:
            self.right_wheel.forward()
        else:
            self.right_wheel.backward()

    def turn_right(self):
        """右转"""
        self.right_wheel.stop()
        if self.direction == FORWARD:
            self.left_wheel.forward()
        else:
            self.left_wheel.backward()

    def forward_left(self):
        """前向左转"""
        self.forward()
        self.turn_left()

    def forward_right(self):
        """前向右转"""
        self.forward()
        self.turn_right()

    def backward_left(self):
        """后向左转"""
        self.backward()
        self.turn_left()

    def backward_right(self):
        """后向右转"""
        self.backward()
        self.turn_right()

    def stop(self):
        """刹车"""
        self.left_wheel.stop()
        self.right_wheel.stop()

    def shutdown(self):
        """熄火"""
        self.stop()
        GPIO.cleanup()


class Driver(object):
    def __init__(self):
        self.car = Car()
        self.server_socket = socket.socket()
        self.server_socket.bind((SERVER_HOST, KEYBOARD_PORT))
        self.server_socket.listen(0)
        self.connection = self.server_socket.accept()[0]
        print("Ready to drive!")

    @staticmethod
    def error():
        """操作码异常"""
        print("Invalid Operation Code!")

    def drive(self):
        """根据操作指令驾驶小车"""
        operations = {
            STOP:               self.car.stop,
            LEFT:               self.car.turn_left,
            RIGHT:              self.car.turn_right,
            FORWARD:            self.car.forward,
            FORWARD | LEFT:     self.car.forward_left,
            FORWARD | RIGHT:    self.car.forward_right,
            BACKWARD:           self.car.backward,
            BACKWARD | LEFT:    self.car.backward_left,
            BACKWARD | RIGHT:   self.car.backward_right,
            SHUTDOWN:           self.car.shutdown
        }
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
            code = struct.unpack('<I', self.connection.recv(struct.calcsize('<I')))[0]
            operations.get(code, self.error)()
            print("Take Action: %s" % code2str.get(code, "None"))
            if code == SHUTDOWN:
                sys.exit(0)


if __name__ == "__main__":
    driver = Driver()
    driver.drive()
