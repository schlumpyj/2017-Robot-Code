#!/usr/bin/env python3
import wpilib
import wpilib.buttons
import ctre
from robotpy_ext.common_drivers import units, navx
from robotpy_ext.autonomous import AutonomousModeSelector
from robotpy_ext.control import button_debouncer
from networktables import NetworkTable
import networktables
class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        """
        Motors
        """
        if not wpilib.RobotBase.isSimulation():
            self.motor1 = ctre.CANTalon(1) #Drive Motors
            self.motor2 = ctre.CANTalon(2)
            self.motor3 = ctre.CANTalon(3)
            self.motor4 = ctre.CANTalon(4)
        else:
            self.motor1 = wpilib.Talon(1) #Drive Motors
            self.motor2 = wpilib.Talon(2)
            self.motor3 = wpilib.Talon(3)
            self.motor4 = wpilib.Talon(4)

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
        self.pistonDown = wpilib.buttons.JoystickButton(self.joystick, 6) #left bumper
        self.pistonUp = wpilib.buttons.JoystickButton(self.joystick, 5) #right bumper
        self.visionEnable = wpilib.buttons.JoystickButton(self.joystick, 3) #X button

        #Controll switch init for auto lock direction
        self.controlSwitch = button_debouncer.ButtonDebouncer(self.joystick, 10, period=0.5)

        #Button for slow reverse out of climb
        self.climbReverseButton = wpilib.buttons.JoystickButton(self.joystick,2)


        self.drivePiston = wpilib.DoubleSolenoid(3,4) #Changes us from mecanum to hi-grip

        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor3, self.motor2)

        """
        All the variables that need to be defined
        """
        self.motorWhere = True #IF IT IS IN MECANUM BY DEFAULT
        self.rotationXbox = 0
        self.rotationPID = 0
        self.firstTime = True
        self.testingAngle = 0
        self.climbVoltage = 0
        self.whichMethod = True
        self.vibrateState = 4
        self.driveViState = 1
        self.strafe_calc = 0

        self.driverStation = wpilib.DriverStation.getInstance()
        """
        Timers
        """
        self.timer = wpilib.Timer()
        self.timer.start()

        self.vibrateTimer = wpilib.Timer()
        self.vibrateTimer.start()

        """
        PIDs
        """
        kP = 0.01
        kI = 0.0001
        kD = 0.00
        kF = 0.00
        turnController = wpilib.PIDController(kP, kI, kD, kF, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController

        kPTwo = 0.01
        kITwo = 0.0001
        kDTwo = 0.00
        kFTwo = 0.00
        autoTurnController = wpilib.PIDController(kPTwo, kITwo, kDTwo, kFTwo, self.navx, output=self)
        autoTurnController.setInputRange(-180.0,  180.0)
        autoTurnController.setOutputRange(-.5, .5)
        autoTurnController.setContinuous(True)
        autoTurnController.setAbsoluteTolerance(2.0)
        self.autoTurnController = autoTurnController

        self.components = {
            'drive': self.robodrive,
            'turner': self.autoTurnController
        }
        self.automodes = AutonomousModeSelector('autonomous',
                                        self.components)
        """
        The great NetworkTables part
        """
        self.vision_table = NetworkTable.getTable('/GRIP/myContoursReport')
        self.vision_x= []
        self.robotStats = NetworkTable.getTable('SmartDashboard')

        self.updater()

    def autonomousPeriodic(self):
        self.automodes.run()

    def teleopInit(self):
        """
            Makes sure the piston is where we think it is
        """
        self.whichMethod = True
        self.firstTime = True
        self.timer.reset()

    def teleopPeriodic(self):
        """
            Human controlled period
            TODO: Have Solenoid being set constantly
        """
        if self.visionEnable.get():
            self.firstTime = True
            self.whichMethod = True

        self.ledRing.set(wpilib.Relay.Value.kOn)

        self.updater()

        if self.pistonUp.get():
            self.motorWhere = False
        elif self.pistonDown.get():
            self.firstTime = True
            self.motorWhere = True

        self.driveStraight()
        self.climb()
        self.vibrator()
        self.alignGear()

        self.total = ((self.joystick.getRawAxis(3)*.65)+.35) # 35% base

        if self.motorWhere==False:
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.robodrive.arcadeDrive(self.total*self.joystick.getY(), self.total*-1*self.joystick.getX(), True)
        elif self.motorWhere==True:
            self.drivePiston.set(wpilib.DoubleSolenoid.Value.kForward)
            if self.visionEnable.get():
                self.robodrive.mecanumDrive_Cartesian(self.strafe_calc, -1*self.rotationXbox, (self.total*self.joystick.getY()), 0)
            else:
                self.robodrive.mecanumDrive_Cartesian((self.total*-1*self.joystick.getX()), -1*self.rotationXbox, (self.total*self.joystick.getY()), 0)

    def driveStraight(self):
        """
            Drive Straight Algorithm to allow mecanums to fly free
        """
        if self.controlSwitch.get():
            self.whichMethod = not self.whichMethod
            if self.whichMethod:
                self.driveViState = 2
            else:
                self.driveViState = 1
            self.vibrateState = 1
            self.firstTime = True

        self.rotationXbox = (self.joystick.getRawAxis(4))*.5

        """
        This toggles between PID control and manual control
        """
        if self.whichMethod:
            if self.rotationXbox < .15 and self.rotationXbox > -.15 and self.firstTime:
                if self.timer.hasPeriodPassed(.5):
                    self.turnController.setSetpoint(self.navx.getYaw())
                    self.firstTime = False
            elif self.rotationXbox < .15 and self.rotationXbox > -.15 and not self.firstTime:
                self.turnController.enable()
                self.rotationXbox=self.rotationPID
            else:
                self.timer.reset()
                self.turnController.disable()
                self.firstTime = True
        else:
            if self.rotationXbox < .15 and self.rotationXbox > -.15:
                self.rotationXbox=0

    def climb(self):
        self.climbVoltage = self.joystick.getRawAxis(2)
        if (self.climbReverseButton.get()):
            #if the climb reverse is active set the motor to reverse
            #multipication to invert values
            self.climb1.set(self.climbVoltage * -1)
            self.climb2.set(self.climbVoltage * -1)
        else:
            #else do as you normally do
            self.climb1.set(self.climbVoltage)
            self.climb2.set(self.climbVoltage)

    def vibrator(self):
        #changed vibrator to pulse istead of long and short because its better
        if (self.vibrateState == 1):
            self.vibrateTimer.reset()
            self.joystick.setRumble(1, .9)
            self.vibrateState = 2
        elif(self.vibrateState == 2):
            if self.vibrateTimer.hasPeriodPassed(0.25):
                #turn off
                self.joystick.setRumble(1, 0)
                self.vibrateState = 3

        elif (self.vibrateState == 3):
            if self.vibrateTimer.hasPeriodPassed(0.50):
                if (self.driveViState == 2):
                    #go around again
                    self.vibrateState = 1
                    self.driveViState = 1
                    #set to its default pos
                else:
                    self.vibrateState = 4 #set to null

    def alignGear(self):
        """
            This is very experimental and is just a test to see if mecanums can work
        """
        try:
            if wpilib.RobotBase.isSimulation():
                self.vision_x=250
            else:
                self.vision_x = self.vision_table.getNumber('centerX', 0)
        except KeyError:
            pass

        if (self.vision_x)!=0:
            if self.vision_x > 180:
                self.strafe_calc=(((self.vision_x-180)/140)*.15)+.15

            elif self.vision_numberX < 150:
                self.strafe_calc=-1*((((150-self.vision_x)/150)*.15)+.15)

    def pidWrite(self, output):

        self.rotationPID = output

    def updater(self):

        self.robotStats.putNumber('PSI', self.psiSensor.getVoltage())

        if self.isAutonomous():
            self.robotStats.putNumber('TIME', (self.driverStation.getMatchTime()+135))
        elif self.isOperatorControl():
            self.robotStats.putNumber('TIME', self.driverStation.getMatchTime())
        else:
            self.robotStats.putNumber('TIME', 150)

if __name__=="__main__":
    wpilib.run(MyRobot)
