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
        
        self.climb1 = wpilib.VictorSP(7)
        self.climb2 = wpilib.VictorSP(8)
        
        """
        Spike Relay for LED
        """
        self.ledRing = wpilib.Relay(0, wpilib.Relay.Direction.kForward) #Only goes forward voltage
        """
        Sensors
        """
        self.navx = navx.AHRS.create_spi()
        self.psiSensor = wpilib.AnalogInput(0)
        self.powerBoard = wpilib.PowerDistributionPanel(0) #Might need or not
        
        self.joystick = wpilib.Joystick(0) #Should be xbox controller
        
        """
        Buttons
        """
        self.pistonDown = wpilib.buttons.JoystickButton(self.joystick, 1) #Will be left bumper
        self.pistonUp = wpilib.buttons.JoystickButton(self.joystick, 2) #Will be right bumper
        self.keepStraight = wpilib.buttons.JoystickButton(self.joystick, 3)
        
        self.drivePiston = wpilib.DoubleSolenoid(3,4) #Changes us from mecanum to hi-grip
        
        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor3, self.motor2) 
        self.motorWhere = True #IF IT IS IN MECANUM BY DEFAULT
        self.rotationXbox = 0
        self.rotationPID = 0
        self.firstTime = True
        self.testingAngle = 0
        self.climbVoltage = 0
        
        """
        Timer
        """
        self.timer = wpilib.Timer()
        self.timer.start()
        """
        PIDs
        """
        kP = 0.01
        kI = 0.00
        kD = 0.00
        kF = 0.00
        turnController = wpilib.PIDController(kP, kI, kD, kF, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController
        
        self.updater()
        
    def teleopInit(self): 
        """"
            Makes sure the piston is where we think it is
        """"
        print ("hello")
        state = self.drivePiston.get()
        if state == wpilib.DoubleSolenoid.Value.kForward:
            self.motorWhere=True
        elif state == wpilib.DoubleSolenoid.Value.kReverse:
            self.motorWhere=False
        else:
            print ("Nope")
        self.timer.reset()
        
    def teleopPeriodic(self):
        """
            Human controlled period
        """
        self.ledRing.set(wpilib.Relay.Value.kOn)
        
        self.updater()
        
        if self.pistonUp.get():
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.motorWhere = False
        elif self.pistonDown.get():
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
            self.motorWhere = True
        
        self.testingAngle = self.testingAngle+(self.joystick.getRawAxis(4)*2) #Maybe multiply by two?
        
        if self.testingAngle >= 180:
            self.testingAngle = self.testingAngle-360
        elif self.testingAngle <= -180:
            self.testingAngle = self.testingAngle+360
        
        if self.keepStraight.get() and self.firstTime:
            self.turnController.setSetpoint(self.navx.getYaw())
            self.firstTime = False
        elif self.keepStraight.get() and not self.firstTime:
            self.turnController.enable()
            self.rotationXbox = self.rotationPID
        else:
            self.firstTime = True
            self.turnController.disable()
            self.rotationXbox = (self.joystick.getRawAxis(4))*.5 #Dead zone that the Xbox controller has
            if self.rotationXbox < .15 and self.rotationXbox > -.15:
                self.rotationXbox=0
            
        self.climb()
        
        self.total = ((self.joystick.getRawAxis(3)*.65)+.35) # 35% base
        
        if self.motorWhere==False:
            self.robodrive.arcadeDrive(self.total*self.joystick.getY(), self.total*-1*self.joystick.getX())
        elif self.motorWhere==True:
            self.robodrive.mecanumDrive_Cartesian((self.total*-1*self.joystick.getX()), -1*self.rotationXbox, (self.total*self.joystick.getY()), 0)

    def climb(self):
        
        self.climbVoltage = self.joystick.getRawAxis(2)
        self.climb1.set(self.climbVoltage)
        self.climb2.set(self.climbVoltage)
            
    def pidWrite(self, output):

        self.rotationPID = output
        
    def updater(self):
        
        wpilib.SmartDashboard.putNumber('PSI', self.psiSensor.getVoltage())
        wpilib.SmartDashboard.putNumber('CAN', self.motor1.getOutputCurrent()) #Just to see what voltage the motors typically go through
        
if __name__=="__main__":
    wpilib.run(MyRobot)
