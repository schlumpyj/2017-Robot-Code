#!/usr/bin/env python3
import wpilib
import wpilib.buttons
import ctre
from components import drive, climb, directions
from misc import vibrator, matchTime
from robotpy_ext.common_drivers import units, navx
from robotpy_ext.autonomous import AutonomousModeSelector
from robotpy_ext.control import button_debouncer
from networktables import NetworkTable
import networktables

class MyRobot(wpilib.IterativeRobot):

    """
        TODO:
            Clean up Drive Straight function if possible
    """


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
        self.gearPistonButton = wpilib.buttons.JoystickButton(self.joystick, 1)
        #Controll switch init for auto lock direction
        self.controlSwitch = button_debouncer.ButtonDebouncer(self.joystick, 10, period=0.5)

        #Button for slow reverse out of climb
        self.climbReverseButton = wpilib.buttons.JoystickButton(self.joystick,2)


        self.drivePiston = wpilib.DoubleSolenoid(3,4) #Changes us from mecanum to hi-grip
        self.gearPiston = wpilib.Solenoid(2)

        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor3, self.motor2)

        self.Drive = drive.Drive(self.robodrive, self.drivePiston, self.navx)
        self.climber = climb.Climb(self.climb1, self.climb2)

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

        """
        Timers
        """
        self.timer = wpilib.Timer()
        self.timer.start()

        self.vibrateTimer = wpilib.Timer()
        self.vibrateTimer.start()

        self.vibrator = vibrator.Vibrator(self.joystick, self.vibrateTimer, .25, .15)



        self.components = {
            'drive': self.Drive
        }

        self.automodes = AutonomousModeSelector('autonomous',
                                        self.components)
        """
        The great NetworkTables part
        """
        self.vision_table = NetworkTable.getTable('/GRIP/myContoursReport')
        self.vision_x= 0
        self.robotStats = NetworkTable.getTable('SmartDashboard')
        self.matchTime = matchTime.MatchTime(self.timer, self.robotStats)
        self.updater()

    def autonomousInit(self):

        self.matchTime.startMode(isAuto=True)

    def autonomousPeriodic(self):

        self.automodes.run()
        self.matchTime.pushTime()

    def teleopInit(self):
        """
            Makes sure the piston is where we think it is
        """
        self.whichMethod = True
        self.firstTime = True
        self.timer.reset()
        self.matchTime.startMode(isAuto=False)

    def teleopPeriodic(self):
        """
            Human controlled period
        """
        self.matchTime.pushTime()

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

        if self.gearPistonButton.get():
            self.gearPiston.set(True)
        else:
            self.gearPiston.set(False)


        self.climbVoltage = self.joystick.getRawAxis(2)
        if (self.climbReverseButton.get()):
            self.climber.climbNow(self.climbVoltage, directions.Direction.kReverse)
        else:
            self.climber.climbNow(self.climbVoltage, directions.Direction.kForward)

        self.driveStraight()
        self.vibrator.runVibrate()
        self.alignGear()

        self.throttle = ((self.joystick.getRawAxis(3)*.65)+.35) # 35% base

        if self.motorWhere==False:

            self.Drive.tankMove(-1*self.joystick.getX(), self.joystick.getY(), self.throttle)

        elif self.motorWhere==True: # Mecanum

            self.Drive.mecanumMove((-1*self.joystick.getX()),self.joystick.getY(), self.rotationXbox, self.throttle)

        else:

            print ("something bad happened")

    def driveStraight(self):
        """
            Drive Straight Algorithm to allow mecanums to fly free
        """
        if self.controlSwitch.get():
            self.whichMethod = not self.whichMethod
            if self.whichMethod:
                self.vibrator.start(2)
            else:
                self.vibrator.start(1)
            self.firstTime = True

        self.rotationXbox = (self.joystick.getRawAxis(4))*.5

        """
        This toggles between PID control and manual control
        """
        if self.whichMethod:
            if self.rotationXbox < .15 and self.rotationXbox > -.15 and self.firstTime:
                if self.timer.hasPeriodPassed(.5):
                    self.Drive.updateSetpoint()
                    self.firstTime = False
                    print ("yo Im here")
            elif self.rotationXbox < .15 and self.rotationXbox > -.15 and not self.firstTime:
                self.Drive.setPIDenable(True)
                print ("I is here my boi")
            else:
                self.timer.reset()
                self.Drive.setPIDenable(False)
                self.firstTime = True
        else:
            if self.rotationXbox < .15 and self.rotationXbox > -.15:
                self.rotationXbox=0
            self.Drive.setPIDenable(False)

    def alignGear(self):
        """
            This is very experimental and is just a test to see if mecanums can work
        """
        try:
            if wpilib.RobotBase.isSimulation():
                self.vision_x=250
            else:
                self.vision_x = self.vision_table.getNumber('centerX', 0)
            if self.visionEnable.get():
                self.Drive.engageVisionX(self.vision_x)
        except KeyError:
            pass

    def updater(self):

        self.robotStats.putNumber('PSI', self.psiSensor.getVoltage())


if __name__=="__main__":
    wpilib.run(MyRobot)
