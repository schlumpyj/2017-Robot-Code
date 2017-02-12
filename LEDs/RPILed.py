#!/usr/bin/python
from networktables import NetworkTable
import pigpio
import time

#Some constants for pins
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

pi = pigpio.pi()
try:
    NetworkTables.initialize(server='10.44.80.2')
    table = NetworkTables.getTable('/SmartDasboard')
except:
    pass

def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

cancel = False
isUp = False
isGear = False
isEnabled = False
REDcounter = 0
BLUEcounter = 0
GREENcounter = 0
states = 0

while not cancel:

    try:
        try:
            isUp = table.getBoolean("State", True)
            isGear = table.getBoolean("Gear", False)
            isEnabled = table.getBoolean("enabled", False)
        except KeyError:
            pass

    except KeyboardInterrupt:

        cancel = True

    if isEnabled:

        if isGear:
            setLights(RED_PIN, 0)
            setLights(BLUE_PIN, 0)
            setLights(GREEN_PIN, 255)

        else:

            if isUp:

                setLights(RED_PIN, 0)
                setLights(BLUE_PIN, 0)
                setLights(GREEN_PIN, 255)

            else:

                setLights(RED_PIN, 255)
                setLights(BLUE_PIN, 255)
                setLights(GREEN_PIN, 0)
    else:

        if states == 0:
            REDCounter +=.01
            BLUECounter +=.01
            if REDCounter > 254:
                BLUECounter = 100
                REDCounter = 100
                states = 1
        if states == 1:
            GREENcounter = 0
            BLUECounter = 0
            REDCounter = 0

        setLights(RED_PIN, REDCounter)
        setLights(BLUE_PIN, BLUECounter)
        setLights(GREEN_PIN, GREENcounter)


pi.stop()
