#!/usr/bin/env python3
class MatchTime(object):

    def __init__(self, timer, table):

        self.timer = timer
        self.startTime = 0
        self.table = table

    def startMode(self, isAuto=False):

        self.isAuto = isAuto
        self.startTime = self.timer.getFPGATimestamp()

    def pushTime(self):

        self.endTime = self.timer.getFPGATimestamp()-self.startTime

        if not self.isAuto:
            self.endTime+=15.0

        self.table.putNumber("TIME", self.endTime)
