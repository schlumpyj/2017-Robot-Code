from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'DDF Place Gear'

    def initialize(self):

        self.speed = -.33

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.mecanumMove(0,0,0,0)
        self.gearPiston.set(False)
    @timed_state(duration=2, next_state='dropGear')
    def drive_forward(self):
        self.drive.mecanumMove(0, 1, 0, self.speed)
        self.gearPiston.set(False)
    @timed_state(duration=.5, next_state='driveBack')
    def dropGear(self):
        self.drive.mecanumMove(0,0,0,0)
        self.gearPiston.set(True)

    @timed_state(duration=.75, next_state="stop")
    def driveBack(self):
        self.drive.mecanumMove(0,-1, 0, self.speed)
        self.gearPiston.set(False)
    @state()
    def stop(self):
        self.drive.mecanumMove(0,0,0,0)
        self.gearPiston.set(False)
