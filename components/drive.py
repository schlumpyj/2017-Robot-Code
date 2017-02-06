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
        self.robotDrive = robotDrive

        kP = 0.01
        kI = 0.0001

        turnController = wpilib.PIDController(kP, kI, 0, 0, self.gyro, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController


        visionP = 0.05 #Likely will have to be much higher

        visionController = wpilib.PIDController(visionP, 0, 0, 0, lambda: self.vision_x, output=self.autoAlignOutput)
        visionController.setInputRange(0.0, 320.0)
        visionController.setOutputRange(-.5, .5)
        visionController.setContinuous(False)
        self.visionController = visionController
        self.visionController.setSetpoint(160.0)

    def mecanumMove(self, x, y, rotation, throttle):

        if not self.turnController.isEnable():
            self.rotation = rotation

        self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
        self.robotDrive.mecanumDrive_Cartesian(throttle*x, self.rotation, throttle*y, 0)

    def tankMove(self, x, y, throttle):

        self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.robotDrive.arcadeDrive(throttle*y, throttle*x)

    def updateSetpoint(self):

        self.turnController.setSetpoint(self.gyro.getYaw())

    def setPIDenable(self, state):

        if state:
            self.turnController.enable()
        else:
            self.turnController.disable()
            self.rotation = 0

    def pidWrite(self, output):

        self.rotation = output

    def engageVisionX(self, value):

        self.visionController.enable()
        self.vision_x = value

    def autoAlignOutput(self, output):

        self.strafe = output
