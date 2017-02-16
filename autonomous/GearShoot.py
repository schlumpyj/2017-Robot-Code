from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Gear Turn-Right Shoot'
    DEFAULT = 'True'

    """
        TODO:
            - Have it floor it to the other side
    """
    def initialize(self):

        self.drive_speed = -0.5

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):

        self.drive.updateSetpoint("auto", 0) #might change back to teleop
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1.75, next_state='startPID')
    def drive_forward(self):

        self.drive.mecanumMove(0,-1,0,.4)

    @state()
    def startPID(self):
        self.drive.updateSetpoint("auto", 65)
        self.drive.setPIDenable(False)
        self.drive.mecanumMove(0,0,0,0)
        self.next_state('stopPID')

    @state()
    def stopPID(self):
        if self.drive.enableAutoTurn():
            self.drive.setPIDenable(True)
            self.drive.updateSetpoint("teleop")
            self.next_state('goForward')

        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1.05, next_state='findPeg')
    def goForward(self):

        self.drive.mecanumMove(0,-1,0,.2)

    @state()
    def findPeg(self):
        self.drive.engageVisionX(True, self.alignGear.getAlignNumber())
        self.drive.mecanumMove(0,0,0,0)

        if self.drive.visionOnTarget():
            self.drive.disableVision()
            self.next_state('goToPeg')

    @state()
    def goToPeg(self):
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("openUp")
        else:
            self.drive.mecanumMove(0,-1,0,.17)

    @timed_state(duration=.75, next_state='goBack')
    def openUp(self):
        self.gearPiston.set(True)

    @timed_state(duration=1, next_state='stop')
    def goBack(self):
        self.gearPiston.set(True)
        self.drive.mecanumMove(0,1,0,.3)

    @state()
    def stop(self):
        self.drive.mecanumMove(0,0,0,0)
