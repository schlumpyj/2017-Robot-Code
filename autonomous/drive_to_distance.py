from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive 114'

    def initialize(self):

        self.speed = -.4

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.mecanumMove(0,0,0,0)
        self.drive.setAutoForwardSetpoint(110)
        self.drive.updateSetpoint("auto", angle=0.0)
        self.drive.setPIDenable(True)

    @state()
    def drive_forward(self):
        #print(self.drive.getSetpoint())
        if self.drive.isAutoForwardOnTarget():
            self.drive.mecanumMove(0,0,0,0)
            self.next_state("stopForNow")
        else:
            self.drive.mecanumMove(0,0,0,0)
        #print (self.drive.getCurrentEncoder())

    @timed_state(duration=0.5, next_state='goToPeg')
    def stopForNow(self):
        self.drive.mecanumMove(0,0,0,0)

    @state()
    def goToPeg(self):
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("stop")
        else:
            self.drive.mecanumMove(0,-1,0,.17)
        print (self.ultrasonic.getRangeInches())
    @state()
    def stop(self):
        self.drive.mecanumMove(0,0,0, 0)
