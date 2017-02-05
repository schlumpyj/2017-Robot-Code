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
        self.robotDrive = robotDrive

        kP = 0.01
        kI = 0.0001
        kD = 0.00
        kF = 0.00

        turnController = wpilib.PIDController(kP, kI, kD, kF, self.gyro, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController

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
