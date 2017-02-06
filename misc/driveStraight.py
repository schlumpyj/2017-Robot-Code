#!/usr/bin/env python3
#Drive straight in a object based form


class driveStraight(object):
  #Main class
  def __init__(self,Timer,WhichMethod,Vibrator,FirstTime,Joystick,drive):
    
    self.timer = Timer #main timer 
    self.whichMethod = WhichMethod #whatever this does?
    self.vibrationClass = Vibrator #the instatiated vibration class form the parent file
    self.thereticalButtonPress = false
    self.firstTime = FirstTime #set first time varible
    self.joystick = Joystick #the joystick
    self.Drive = drive #drive passed
    
    self.rotationXbox = 0
    
  def setWhichVariable(self,var):
    self.whichMethod = var #update
    
  def setFirstTimeVariable(self,var):
    self.firstTime = var
    
  def PressButton(self):
    self.thereticalButtonPress = true
    
  def driveStraight(self):

    #On provided button down down
    if self.thereticalButtonPress = true:
      #set to false
      self.thereticalButtonPress = false

      self.whichMethod = not self.whichMethod
      if self.whichMethod:
        self.vibrator.start(2)
      else:
        self.vibrator.start(1)
      self.firstTime = True
      
    self.rotationXbox = (self.joystick.getRawAxis(4))*.5

        
        This toggles between PID control and manual control
        
        if self.whichMethod:
            if self.rotationXbox < .15 and self.rotationXbox > -.15 and self.firstTime:
                if self.timer.hasPeriodPassed(.5):
                    self.Drive.updateSetpoint()
                    self.firstTime = False
            elif self.rotationXbox < .15 and self.rotationXbox > -.15 and not self.firstTime:
                self.Drive.setPIDenable(True)
            else:
                self.timer.reset()
                self.Drive.setPIDenable(True)
                self.firstTime = True
        else:
            if self.rotationXbox < .15 and self.rotationXbox > -.15:
    self.rotationXbox=0
    
"""
old code:

 def driveStraight(self):
        
            Drive Straight Algorithm to allow mecanums to fly free
        
        if self.controlSwitch.get():
            self.whichMethod = not self.whichMethod
            if self.whichMethod:
                self.vibrator.start(2)
            else:
                self.vibrator.start(1)
            self.firstTime = True

 self.rotationXbox = (self.joystick.getRawAxis(4))*.5

        
        This toggles between PID control and manual control
        
        if self.whichMethod:
            if self.rotationXbox < .15 and self.rotationXbox > -.15 and self.firstTime:
                if self.timer.hasPeriodPassed(.5):
                    self.Drive.updateSetpoint()
                    self.firstTime = False
            elif self.rotationXbox < .15 and self.rotationXbox > -.15 and not self.firstTime:
                self.Drive.setPIDenable(True)
            else:
                self.timer.reset()
                self.Drive.setPIDenable(True)
                self.firstTime = True
        else:
            if self.rotationXbox < .15 and self.rotationXbox > -.15:
self.rotationXbox=0
"""
