from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'DF Place Gear'

    def initialize(self):

        self.speed = -.4

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.tankMove(0,0,0)
        self.gearPiston.set(False)
    @timed_state(duration=2, next_state='dropGear')
    def drive_forward(self):
        self.drive.tankMove(0, 1, self.speed)
        self.gearPiston.set(False)
    @timed_state(duration=.5, next_state='driveBack')
    def dropGear(self):
        self.drive.tankMove(0,0,0)
        self.gearPiston.set(True)

    @timed_state(duration=1, next_state="stop")
    def driveBack(self):
        self.drive.tankMove(0,-1,self.speed)
        self.gearPiston.set(False)
    @state()
    def stop(self):
        self.drive.tankMove(0,0,0)
        self.gearPiston.set(False)
