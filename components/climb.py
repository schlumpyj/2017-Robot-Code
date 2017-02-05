#!/usr/bin/env python3
import wpilib

class Climb(object):


    def __init__(self, motor1, motor2):

        self.motor1 = motor1
        self.motor2 = motor2
        self.direction = 1

    def climbNow(self, speed, direction):

        self.motor1.set(direction.value*speed)
        self.motor2.set(direction.value*speed)
