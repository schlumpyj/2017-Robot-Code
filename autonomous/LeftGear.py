from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Turn-Left Gear'

    """
        TODO:
            - Have it floor it to the other side
            - Adjust angle and distance
    """
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,0,0,0)
        self.drive.setAutoForwardSetpoint(85)
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
    @timed_state(duration=.5, next_state="startPID")
    def wait(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,0,0,0)
    @state()
    def startPID(self):
        self.gearPiston.set(False)
        self.drive.updateSetpoint("auto", -58)
        self.drive.setPIDenable(False)
        self.drive.mecanumMove(0,0,0,0)
        self.next_state('stopPID')

    @timed_state(duration=3, next_state="stop")
    def stopPID(self):
        if self.drive.enableAutoTurn():
            self.drive.setPIDenable(True)
            self.drive.updateSetpoint("teleop")
            self.next_state('goForward')
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,0,0,0)

    @timed_state(duration=1.05, next_state='findPeg')
    def goForward(self):
        self.gearPiston.set(False)
        self.drive.turnLightOn()
        self.drive.mecanumMove(0,1,0,.2)
        self.drive.disableAutoForward()
        self.drive.disableAutoTurn()

    @timed_state(duration=3, next_state="stop")
    def findPeg(self):
        self.gearPiston.set(False)
        self.drive.engageVisionX(True, self.alignGear.getAlignNumber())
        if self.drive.visionOnTarget():
            self.drive.disableVision()
            self.next_state('goToPeg')
        self.drive.mecanumMove(0,0,0,0)
    @timed_state(duration=2.5, next_state="openUp")
    def goToPeg(self):
        self.gearPiston.set(False)
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("openUp")
        else:
            self.drive.disableVision()
            self.drive.disableAutoForward() #This is likly the problem for not moving forward
            self.drive.disableAutoTurn()
            self.drive.mecanumMove(0,-1,0,.27)
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
    @timed_state(duration=1, next_state="goBackInit")
    def pushGear(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,-1,0,.23)
    @timed_state(duration=1.5, next_state="stop")
    def goBackInit(self):
        self.gearPiston.set(False)
        self.drive.mecanumMove(0,1,0,.23)
    @state()
    def stop(self):
        self.drive.mecanumMove(0,0,0,0)
