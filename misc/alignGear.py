from networktables import Networktable

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
            return 0 #should really return an error message or something
