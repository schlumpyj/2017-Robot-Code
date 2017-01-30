from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Gear Turn-Right Shoot'
    DEFAULT = 'True'

    def initialize(self):

        self.drive_speed = 0.5
        self.rotationPID = 0

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.drive(0,0) #Wait a little bit

    @timed_state(duration=2, next_state='startPID')
    def drive_forward(self):
        self.drive.drive(self.drive_speed, 0)

    @state()
    def startPID(self):
        self.turner.setSetpoint(30)
        self.turner.enable()
        self.drive.drive(0,0)
        self.next_state('stopPID')


    @state()
    def stopPID(self):
        if self.turner.onTarget():
            self.turner.disable()
            self.drive.drive(0,0)
            self.next_state('hold')
        else:
            self.drive.mecanumDrive_Cartesian(0, -1*self.rotationPID, 0, 0)

    @timed_state(duration=0.5, next_state='goBack')
    def hold(self):
        self.drive.drive(0,0)

    @timed_state(duration=1.5)
    def goBack(self):
        self.drive.drive(self.drive_speed, 0)

    def pidWrite(self, output):
        self.rotationPID = output
