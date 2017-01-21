#!/usr/bin/env python3
import wpilib
import ctre
import wpilib.buttons
from networktables import NetworkTable
import networktables
class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.motor1 = ctre.CANTalon(1)
        self.motor2 = ctre.CANTalon(2)
        self.motor3 = ctre.CANTalon(3)
        self.motor4 = ctre.CANTalon(4)
        self.joystick = wpilib.Joystick(0)
        self.pistonDown = wpilib.buttons.JoystickButton(self.joystick, 1)
        self.pistonUp = wpilib.buttons.JoystickButton(self.joystick, 2)
        self.drivePiston = wpilib.DoubleSolenoid(3,4)
        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor2, self.motor3)
        self.motorWhere = False
    def teleopPeriodic(self):
        if self.pistonUp.get():
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.motorWhere = False
        elif self.pistonDown.get():
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
            self.motorWhere = True
        self.total = (self.joystick.getRawAxis(3)*.75)+.25
        if self.motorWhere==False: 
            self.robodrive.arcadeDrive(self.total*self.joystick.getY(), self.total*-1*self.joystick.getX())
        elif self.motorWhere==True:
            self.robodrive.mecanumDrive_Cartesian(self.joystick.getX(), self.joystick.getY(), self.joystick.getRawAxis(4), 0)
            


if __name__=="__main__":
    wpilib.run(MyRobot)

