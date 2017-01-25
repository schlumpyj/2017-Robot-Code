#!/usr/bin/env python3
import wpilib
import ctre
import wpilib.buttons
from robotpy_ext.common_drivers import units, navx
from networktables import NetworkTable
import networktables

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        """
        Motors
        """
        self.motor1 = ctre.CANTalon(1) #Drive Motors
        self.motor2 = ctre.CANTalon(2) 
        self.motor3 = ctre.CANTalon(3)
        self.motor4 = ctre.CANTalon(4)
        
        """
        Sensors
        """
        self.navx = navx.AHRS.create_spi()
        
        self.joystick = wpilib.Joystick(0)#Should be xbox controller
        
        """
        Buttons
        """
        self.pistonDown = wpilib.buttons.JoystickButton(self.joystick, 1) #Will be left bumper
        self.pistonUp = wpilib.buttons.JoystickButton(self.joystick, 2) #Will be right bumper
        self.keepStraight = wpilib.buttons.JoystickButton(self.joystick, 3)
        
        self.drivePiston = wpilib.DoubleSolenoid(3,4) #Changes us from mecanum to hi-grip
        
        #self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor2, self.motor3) 
        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor3, self.motor2) 
        self.motorWhere = True #IF IT IS IN MECANUM BY DEFAULT
        self.rotationXbox = 0
        self.rotationPID = 0
        self.firstTime = True
        
        """
        PIDs
        """
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00
        turnController = wpilib.PIDController(kP, kI, kD, kF, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController
        
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
        
        if self.keepStraight.get() and self.firstTime:
            self.turnController.setSetpoint(self.navx.getYaw())
            self.firstTime = False
        elif self.keepStraight.get() and not self.firstTime:
            self.turnController.enable()
            #self.rotationXbox = self.rotationPID
        else:
            self.firstTime = True
            self.turnController.disable()
            self.rotationXbox = self.joystick.getRawAxis(4) #Dead zone that the Xbox controller has

       
        self.rotationXbox = self.joystick.getRawAxis(4)
        if self.rotationXbox < .15 and self.rotationXbox > -.15:
            self.rotationXbox=0
        self.total = -1*((self.joystick.getRawAxis(3)*.65)+.35) # 35% base
        
        if self.motorWhere==True:
            #print ("tank")
            self.robodrive.arcadeDrive(self.total*self.joystick.getY(), self.total*-1*self.joystick.getX())
        elif self.motorWhere==False:
            #print ("Mec")
            #self.robodrive.mecanumDrive_Cartesian((self.total*self.joystick.getX()),self.rotationXbox,(self.total*self.joystick.getY()) , 0)
            self.robodrive.mecanumDrive_Cartesian((self.total*-1*self.joystick.getX()), self.rotationXbox, (self.total*self.joystick.getY()), 0)

    def pidWrite(self, output):

        self.rotationPID = output
        
if __name__=="__main__":
    wpilib.run(MyRobot)
