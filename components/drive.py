#!/usr/bin/env python3
import wpilib

class Drive(object):

    """
    My attempt at using OOP
    """

    def __init__(self, robotDrive, drivePiston, gyro, encoder):

        self.drivePiston = drivePiston
        self.rotation = 0
        self.gyro = gyro
        self.vision_x = 0
        self.strafe = 0
        self.encoder = encoder
        self.rotateAuto = 0
        self.forward = 0
        self.robotDrive = robotDrive

        self.encoder.setDistancePerPulse(.106103)
        self.encoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)


        kP = 0.01
        kI = 0.0001

        turnController = wpilib.PIDController(kP, kI, 0, 0, self.gyro, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController


        visionP = 0.09 #Likely will have to be much higher

        visionController = wpilib.PIDController(visionP, 0, 0, 0, lambda: self.vision_x, output=self.autoAlignOutput)
        visionController.setInputRange(0.0, 320.0)
        visionController.setOutputRange(-.5, .5)
        visionController.setContinuous(False)
        visionController.setPercentTolerance(.5)
        self.visionController = visionController
        self.visionController.setSetpoint(190.0)

        autoP = 0.1

        autoTurn = wpilib.PIDController(autoP, 0, 0, 0, self.gyro, output=self.autoTurnOutput)
        autoTurn.setInputRange(-180.0,  180.0)
        autoTurn.setOutputRange(-.25, .25)
        autoTurn.setContinuous(True)
        autoTurn.setPercentTolerance(2)
        self.autoTurn = autoTurn

        autoForwardP = 0.02 #I have no idea if this is good enough

        autoForward = wpilib.PIDController(autoForwardP, 0, 0, 0, self.encoder, output=self.autoForwardOutput)
        autoForward.setInputRange(0, 180.0) #I don't know what to put for the input range
        autoForward.setOutputRange(-.4, .4)
        autoForward.setContinuous(False)
        autoForward.setPercentTolerance(.5)
        self.autoForward = autoForward


    """
    Mecanum and tank functions
    """

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

        if not self.autoForward.isEnable():
            self.forward = throttle*y

        self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
        self.robotDrive.mecanumDrive_Cartesian(self.strafe, -1*self.rotation, self.forward, 0)

    def tankMove(self, x, y, throttle):

        self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.robotDrive.arcadeDrive(throttle*y, throttle*x, True)

    """
    Main PID Control for mostly teleop driving
    """
    def setPIDenable(self, state):

        if state:
            self.turnController.enable()
        else:
            self.turnController.disable()
            self.rotation = 0

    def updateSetpoint(self, controller, angle=0):
        if controller == "teleop":
            self.turnController.setSetpoint(self.gyro.getYaw())
        elif controller == "auto":
            print (angle)
            self.autoTurn.setSetpoint(angle)

    def getSetpoint(self):
        return self.turnController.getSetpoint()

    """
    Auto Turn variables
    """
    def enableAutoTurn(self):

        self.autoTurn.enable()
        if self.autoTurn.onTarget():
            self.autoTurn.disable()
            return True

    def getAutoSetpoint(self):
        return self.autoTurn.getSetpoint()


    """
    Vision Side to Side Stuff
    """

    def engageVisionX(self, state, value):
        if state:
            self.visionController.enable()
            self.vision_x = value
            #print (self.vision_x)
        else:
            self.visionController.disable()

    def visionOnTarget(self):

        if self.visionController.onTarget():
            print (self.vision_x)
            print ("Im on target!")
            return True

    def disableVision(self):

        self.visionController.disable()
        self.autoTurn.disable()


    """
    Encoder PID and stuff
    """
    def getCurrentEncoder(self):
        return self.encoder.getDistance()

    def resetEncoder(self):
        self.encoder.reset()

    def setAutoForwardSetpoint(self, setpoint):

        self.autoForward.setSetpoint(setpoint)

    def isAutoForwardOnTarget(self):

        if self.autoForward.onTarget():
            self.autoForward.disable()
            return True

        else:
            self.autoForward.enable()

    def disableAutoForward(self):
        self.autoForward.disable()



    """
    All the PID Write functions...nothing to really see here
    """

    def pidWrite(self, output):

        self.rotation = output

    def autoAlignOutput(self, output):

        self.strafe = output

    def autoTurnOutput(self, output):

        self.rotateAuto = output

    def autoForwardOutput(self, output):

        self.forward = -1 * output
