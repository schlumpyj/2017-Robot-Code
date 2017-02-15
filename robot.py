#!/usr/bin/env python3
import wpilib
import wpilib.buttons
from components import drive, climb, directions
from misc import vibrator, matchTime, driveStraight, alignGear
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
            import ctre
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

        self.joystick = wpilib.Joystick(0) #xbox controller

        wpilib.CameraServer.launch('misc/vision.py:main')
        """
        Buttons
        """
        self.visionEnable = wpilib.buttons.JoystickButton(self.joystick, 4) #X button
        self.gearPistonButton = wpilib.buttons.JoystickButton(self.joystick, 6)
        self.safetyPistonButton = wpilib.buttons.JoystickButton(self.joystick, 3)
        #Controll switch init for auto lock direction
        self.controlSwitch = button_debouncer.ButtonDebouncer(self.joystick, 10, period=0.5)
        #for drive toggle
        self.driveControlButton = button_debouncer.ButtonDebouncer(self.joystick,5, period=0.5)

        #Button for slow reverse out of climb
        self.climbReverseButton = wpilib.buttons.JoystickButton(self.joystick,2)


        self.drivePiston = wpilib.DoubleSolenoid(3,4) #Changes us from mecanum to hi-grip
        self.gearPiston = wpilib.Solenoid(2)
        self.safetyPiston = wpilib.Solenoid(1)

        self.robodrive = wpilib.RobotDrive(self.motor1, self.motor4, self.motor3, self.motor2)

        self.Drive = drive.Drive(self.robodrive, self.drivePiston, self.navx)
        self.climber = climb.Climb(self.climb1, self.climb2)

        """
        All the variables that need to be defined
        """
        self.motorWhere = True #IF IT IS IN MECANUM BY DEFAULT
        self.rotationXbox = 0
        self.climbVoltage = 0
        """
        Timers
        """
        self.timer = wpilib.Timer()
        self.timer.start()

        self.vibrateTimer = wpilib.Timer()
        self.vibrateTimer.start()

        self.vibrator = vibrator.Vibrator(self.joystick, self.vibrateTimer, .25, .15)

        self.encoder = wpilib.Encoder(2, 3)
        self.encoder.setDistancePerPulse(2)

        """
        The great NetworkTables part
        """
        self.vision_table = NetworkTable.getTable('/GRIP/myContoursReport')
        self.alignGear = alignGear.AlignGear(self.vision_table)
        self.robotStats = NetworkTable.getTable('SmartDashboard')
        self.matchTime = matchTime.MatchTime(self.timer, self.robotStats)

        self.robotStats.putBoolean("enabled", False)
        self.robotStats.putString("Gear", "nope")
        """
        Drive Straight
        """
        self.DS = driveStraight.driveStraight(self.timer, self.vibrator, self.Drive, self.robotStats)

        self.components = {
            'drive': self.Drive,
            'alignGear': self.alignGear,
            'gearPiston': self.gearPiston
        }

        self.automodes = AutonomousModeSelector('autonomous',
                                        self.components)
        self.updater()

    def autonomousInit(self):

        self.matchTime.startMode(isAuto=True)
        self.navx.reset()
        self.robotStats.putBoolean("enabled", True)

    def autonomousPeriodic(self):

        self.automodes.run()
        self.matchTime.pushTime()
        self.ledRing.set(wpilib.Relay.Value.kOn)
        
    def teleopInit(self):
        """
            Makes sure the piston is where we think it is
        """

        self.ledRing.set(wpilib.Relay.Value.kOn) #I don't think it needs to be in the teleopPeriodic

        self.DS.setWhichVariable(True)
        self.Drive.updateSetpoint("teleop")
        self.Drive.disableVision()
        self.DS.setFirstTimeVariable(True)
        self.timer.reset()
        self.matchTime.startMode(isAuto=False)
        self.robotStats.putBoolean("enabled", True)

    def teleopPeriodic(self):
        """
            Human controlled period
        """
        print (self.encoder.getRate())
        self.matchTime.pushTime()

        if self.visionEnable.get():
            self.DS.setFirstTimeVariable(True)
            self.DS.setWhichVariable(True)

        self.updater()

        if (self.driveControlButton.get()):
            self.motorWhere = not self.motorWhere

        if self.gearPistonButton.get():
            self.gearPiston.set(True)
        else:
            self.gearPiston.set(False)

        if self.safetyPistonButton.get():
            self.safetyPiston.set(False)
        else:
            self.safetyPiston.set(True)

        self.rotationXbox = (self.joystick.getRawAxis(4))*.5

        self.climbVoltage = self.joystick.getRawAxis(2)
        if (self.climbReverseButton.get()):
            self.climber.climbNow(self.climbVoltage, directions.Direction.kReverse)
        else:
            self.climber.climbNow(self.climbVoltage, directions.Direction.kForward)

        if self.controlSwitch.get():
            self.DS.PressButton()

        if self.visionEnable.get():
            self.Drive.engageVisionX(True, self.alignGear.getAlignNumber())
        else:
            self.Drive.disableVision()

        self.DS.driveStraight(self.rotationXbox)
        self.vibrator.runVibrate()

        self.throttle = ((self.joystick.getRawAxis(3)*.65)+.35) # 35% base

        if self.motorWhere==False: #tank
            self.robotStats.putString("State", "tank")
            self.Drive.tankMove(-1*self.joystick.getX(), self.joystick.getY(), self.throttle)
            self.Drive.updateSetpoint("teleop") #should fix angle error

        elif self.motorWhere==True: # Mecanum
            self.robotStats.putString("State", "mecanum")
            self.Drive.mecanumMove((-1*self.joystick.getX()),self.joystick.getY(), self.rotationXbox, self.throttle)

        else:
            print ("something bad happened")

    def disabledPeriodic(self):
        self.robotStats.putBoolean("enabled", False)
        self.updater()

    def updater(self):

        self.robotStats.putNumber('PSI', self.psiSensor.getVoltage())

if __name__=="__main__":
    wpilib.run(MyRobot)
