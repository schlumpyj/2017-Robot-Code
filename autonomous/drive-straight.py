from robotpy_ext.autonomous import StatefulAutonomous, timed_state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'

    def initialize(self):

        self.speed = .4

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.tankMove(0,0,0)

    @timed_state(duration=2)
    def drive_forward(self):
        self.drive.tankMove(0, 1, self.speed)
