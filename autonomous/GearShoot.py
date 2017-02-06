from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Gear Turn-Right Shoot'
    DEFAULT = 'True'

    def initialize(self):

        self.drive_speed = 0.5

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.mecanumMove(0,0,0,0) #Wait a little bit

    @timed_state(duration=2, next_state='startPID')
    def drive_forward(self):
        self.drive.mecanumMove(0,0,1,.3)

    @state()
    def startPID(self):
        self.drive.updateSetpoint("auto", angle=30)
        self.drive.mecanumMove(0,0,0,0)
        self.next_state('stopPID')
    @state()
    def stopPID(self):
        if self.drive.enableAutoTurn():
            self.drive.mecanumMove(0,0,0,0)
            self.next_state('hold')
        else:
            self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=0.5, next_state='goBack')
    def hold(self):
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1.5)
    def goBack(self):
        self.drive.mecanumMove(0,0,-1, .3)
