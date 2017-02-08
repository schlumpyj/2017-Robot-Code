#!/usr/bin/env python3
import wpilib

class Drive(object):

    """
    My attempt at using OOP
    """

    def __init__(self, robotDrive, drivePiston, gyro):

        self.drivePiston = drivePiston
        self.rotation = 0
        self.gyro = gyro
        self.vision_x = 0
        self.strafe = 0
        self.rotateAuto = 0
        self.robotDrive = robotDrive

        kP = 0.01
        kI = 0.0001

        turnController = wpilib.PIDController(kP, kI, 0, 0, self.gyro, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController


        visionP = 0.01 #Likely will have to be much higher

        visionController = wpilib.PIDController(visionP, 0, 0, 0, lambda: self.vision_x, output=self.autoAlignOutput)
        visionController.setInputRange(0.0, 320.0)
        visionController.setOutputRange(-.5, .5)
        visionController.setContinuous(False)
        visionController.setPercentTolerance(4)
        self.visionController = visionController
        self.visionController.setSetpoint(160.0)

        autoP = 0.03

        autoTurn = wpilib.PIDController(visionP, 0, 0, 0, self.gyro, output=self.autoTurnOutput)
        autoTurn.setInputRange(-180.0,  180.0)
        autoTurn.setOutputRange(-.25, .25)
        autoTurn.setContinuous(True)
        autoTurn.setPercentTolerance(3)
        self.autoTurn = autoTurn


    def mecanumMove(self, x, y, rotation, throttle):

        if not self.turnController.isEnable():
            if rotation < .15 and rotation > -.15:
                 self.rotation = 0
            else:
                 self.rotation = rotation
            self.rotation = rotation

        if self.autoTurn.isEnable():
            self.rotation = self.rotateAuto

        if not self.visionController.isEnable():
            self.strafe = throttle*x

        self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
        self.robotDrive.mecanumDrive_Cartesian(self.strafe, -1*self.rotation, throttle*y, 0)

    def tankMove(self, x, y, throttle):

        self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.robotDrive.arcadeDrive(throttle*y, throttle*x, True)

    def updateSetpoint(self, controller, angle=0):
        if controller == "teleop":
            self.turnController.setSetpoint(self.gyro.getYaw())
        elif controller == "auto":
            self.autoTurn.setSetpoint(angle)

    def enableAutoTurn(self):

        self.autoTurn.enable()
        if self.autoTurn.onTarget():
            self.autoTurn.disable()
            return True

    def setPIDenable(self, state):

        if state:
            self.turnController.enable()
        else:
            self.turnController.disable()
            self.rotation = 0

    def engageVisionX(self, state, value):
        if state:
            if self.visionController.isEnable():
                return True
            self.visionController.enable()
            self.vision_x = value
            print (self.vision_x)
        else:
            self.visionController.disable()

    def disableVision(self):
        self.visionController.disable()

    def pidWrite(self, output):

        self.rotation = output

    def autoAlignOutput(self, output):

        self.strafe = output

    def autoTurnOutput(self, output):

        self.rotateAuto = output
