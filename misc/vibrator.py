#!/usr/bin/env python3
class Vibrator(object):

    def __init__(self, joystick, timer, vibratePeriod, stopPeriod, amps=.9):

        self.joystick = joystick
        self.timer = timer
        self.state = 5
        self.frequency = 0
        self.vibratePeriod = vibratePeriod
        self.stopPeriod = stopPeriod
        self.amps = amps
        self.counter = 0

    def start(self, frequency):

        self.state = 1
        self.counter = 0
        self.frequency = frequency

    def runVibrate(self):

        if self.state == 1:
            self.timer.reset()
            self.joystick.setRumble(1, self.amps)
            self.state = 2
        elif self.state == 2:
            if self.timer.hasPeriodPassed(self.vibratePeriod):
                self.joystick.setRumble(1, 0)
                self.state = 3
        elif self.state == 3:
            if self.timer.hasPeriodPassed(self.stopPeriod):
                self.state=4
        elif self.state == 4:
            self.counter+=1
            if self.counter == self.frequency:
                self.state = 5 #Dead state
            else:
                self.state = 1
