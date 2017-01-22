#!/usr/bin/env python3
import wpilib
import ctre
import wpilib.buttons
from networktables import NetworkTable
import networktables

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        """
        Set up code
        """
        self.motor1 = ctre.CANTalon(1) #Drive Motors
        self.motor2 = ctre.CANTalon(2) 
        self.motor3 = ctre.CANTalon(3)
        self.motor4 = ctre.CANTalon(4)
        
        self.joystick = wpilib.Joystick(0)#Should be xbox controller
        
        self.pistonDown = wpilib.buttons.JoystickButton(self.joystick, 1) #Will be left bumper
        self.pistonUp = wpilib.buttons.JoystickButton(self.joystick, 2) #Will be right bumper
        
        self.drivePiston = wpilib.DoubleSolenoid(3,4) #Changes us from mecanum to hi-grip
        
        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor2, self.motor3) 
        
        self.motorWhere = True #IF IT IS IN MECANUM BY DEFAULT
    
    def teleopPeriodic(self):
        """
            Human controlled period
        """
        
        if self.pistonUp.get():
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.motorWhere = False
        elif self.pistonDown.get():
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
            self.motorWhere = True
        
        self.total = -1*((self.joystick.getRawAxis(3)*.65)+.35) # 35% base
        
        if self.motorWhere==False: 
            self.robodrive.arcadeDrive(self.total*self.joystick.getY(), self.total*-1*self.joystick.getX())
        elif self.motorWhere==True:
            self.robodrive.mecanumDrive_Cartesian((-1*self.joystick.getX()), (-1*self.joystick.getY()), self.joystick.getRawAxis(4), 0)
            


if __name__=="__main__":
    wpilib.run(MyRobot)

