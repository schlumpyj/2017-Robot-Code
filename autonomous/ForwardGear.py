from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Forward Gear'

    def initialize(self):

        self.speed = -.4

    @timed_state(duration=0.5, next_state='goToPeg', first=True)
    def drive_wait(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,0,0,0)
        self.drive.setAutoForwardSetpoint(92)
        self.drive.updateSetpoint("teleop")
        self.drive.setPIDenable(True)

    @timed_state(duration=4, next_state="stop")
    def goToPeg(self):
        self.gearPiston.set(False)
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("openUp")
        else:
            self.drive.mecanumMove(0,-1,0,.3)
        print (self.ultrasonic.getRangeInches())

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
