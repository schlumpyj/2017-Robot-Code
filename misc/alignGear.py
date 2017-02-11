from networktables import NetworkTable
import wpilib
import wpilib.buttons
class AlignGear(object):

    def __init__(self, table):

        self.vision_x = 0
        self.table = table

    def getAlignNumber(self):

        try:
            if wpilib.RobotBase.isSimulation():
                self.vision_x=250
            else:
                self.vision_x = self.table.getNumber('centerX', 0)
            return self.vision_x
        except KeyError:
            return 160 #should really return an error message or something
