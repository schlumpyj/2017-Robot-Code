#!/usr/bin/env python3
#Drive straight in a object based form
class driveStraight(object):

    def __init__(self, timer, whichMethod, vibrator, firstTime, drive):

        self.timer = timer #main timer
        self.whichMethod = whichMethod #whatever this does?
        self.vibrator = vibrator #the instatiated vibration class form the parent file
        self.thereticalButtonPress = False
        self.firstTime = firstTime #set first time varible
        self.Drive = drive #drive passed

    def setWhichVariable(self, var):
        self.whichMethod = var #update

    def setFirstTimeVariable(self, var):
        self.firstTime = var

    def PressButton(self):
        self.thereticalButtonPress = True

    def driveStraight(self, rotationValue):

        #On provided button down down
        if self.thereticalButtonPress == True:
            #set to false
            self.thereticalButtonPress = False

            self.whichMethod = not self.whichMethod
            if self.whichMethod:
                self.vibrator.start(2)
            else:
                self.vibrator.start(1)
            self.firstTime = True

        """
        This toggles between PID control and manual control
        """
        if self.whichMethod:
            if rotationValue < .15 and rotationValue > -.15 and self.firstTime:
                if self.timer.hasPeriodPassed(.5):
                    self.Drive.updateSetpoint("teleop")
                    self.firstTime = False
            elif rotationValue < .15 and rotationValue > -.15 and not self.firstTime:
                self.Drive.setPIDenable(True)
            else:
                self.timer.reset()
                self.Drive.setPIDenable(False)
                self.firstTime = True
        else:

            self.Drive.setPIDenable(False)
