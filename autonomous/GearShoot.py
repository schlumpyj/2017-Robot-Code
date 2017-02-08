from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Gear Turn-Right Shoot'
    DEFAULT = 'True'

    def initialize(self):
        
        self.drive_speed = -0.5

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        #print ("yo")
        self.drive.mecanumMove(0,0,0,0) #Wait a little bit

    @timed_state(duration=1.5, next_state='startPID')
    def drive_forward(self):
        #print ("yo")
        self.drive.mecanumMove(0,-1,0,.2)

    @state()
    def startPID(self):
        self.drive.updateSetpoint("auto", 45)
        self.drive.mecanumMove(0,0,0,0)
        self.next_state('stopPID')

        
    @state()
    def stopPID(self):
        if self.drive.enableAutoTurn():
            self.drive.mecanumMove(0,0,0,0)
            self.next_state('goForward')
        else:
            self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1, next_state='findPeg')
    def goForward(self):
        self.drive.mecanumMove(0,-1,0,.2)

    @timed_state(duration=3, next_state='hold')
    def findPeg(self):
        self.drive.engageVisionX(True, self.alignGear.getAlignNumber())
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1.5, next_state='goBack')
    def hold(self):
        self.drive.disableVision()
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1.5, next_state='stop')
    def goBack(self):
        self.drive.mecanumMove(0,0,0, 0)

    @state()
    def stop(self):
        self.drive.mecanumMove(0,0,0,0)
