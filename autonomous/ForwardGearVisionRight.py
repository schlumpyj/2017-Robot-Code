from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Forward Gear Vision Right'

    def initialize(self):

        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,0,0,0)
        self.drive.setAutoForwardSetpoint(65)
        self.drive.updateSetpoint("teleop")
        self.drive.setPIDenable(True)

    @timed_state(duration=1.75, next_state='wait')
    def drive_forward(self):
        self.gearPiston.set(False)
        if self.drive.isAutoForwardOnTarget():
            self.drive.mecanumMove(0,0,0,0)
            self.drive.disableAutoForward()
            self.next_state("wait")
        else:
            self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=.5, next_state="findPeg")
    def wait(self):
        self.drive.disableAutoForward()
        self.drive.disableAutoTurn()
        self.drive.turnLightOn()
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=3, next_state="stop")
    def findPeg(self):
        self.gearPiston.set(False)
        self.drive.engageVisionX(True, self.alignGear.getAlignNumber())
        if self.drive.visionOnTarget():
            self.drive.disableVision()
            self.next_state('goToPeg')
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=4, next_state="stop")
    def goToPeg(self):
        self.gearPiston.set(False)
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("openUp")
        else:
            self.drive.mecanumMove(0,-1,0,.3)
        print (self.ultrasonic.getRangeInches())

    @timed_state(duration=.6, next_state='backWhileOpen')
    def openUp(self):
        self.gearPiston.set(True)
        self.drive.mecanumMove(0,0,0,0)
        self.drive.disableAutoForward()

    @timed_state(duration=1, next_state='pushGear')
    def backWhileOpen(self):
        self.gearPiston.set(True)
        self.drive.mecanumMove(0,1,0,.2)
    @timed_state(duration=1, next_state="backAfterPush")
    def pushGear(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,-1,0,.23)
    @timed_state(duration=1, next_state="strafeRight")
    def backAfterPush(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,1,0,.3)

    @timed_state(duration=2, next_state="onWards")
    def strafeRight(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(-1,0,0,.7)

    @timed_state(duration=2, next_state="stop")
    def onWards(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,-1,0,.5)
    @state()
    def stop(self):
        self.drive.mecanumMove(0,0,0,0)
