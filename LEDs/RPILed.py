#!/usr/bin/python
from networktables import NetworkTable
import pigpio
import time
import colorsys

#Some constants for pins
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

pi = pigpio.pi()

NetworkTable.initialize(server='10.44.80.2')
table = NetworkTable.getTable('/SmartDasboard')

def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(255) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

cancel = False
isUp = False
isGear = False
isEnabled = False
counter = 0

while not cancel:

    try:
        try:
            isUp = table.getBoolean("State", True)
            isGear = table.getBoolean("Gear", False)
            isEnabled = table.getBoolean("enabled", False)
        except KeyError:
            pass

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
        counter+=.00005
        if counter > 1.00:
            counter = 0
        output = colorsys.hsv_to_rgb(counter, 1, 1)
        setLights(RED_PIN, (output[0]*255))
        setLights(GREEN_PIN, (output[1]*255))
        setLights(BLUE_PIN, (output[2]*255))


    except KeyboardInterrupt:

        cancel = True
setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)
pi.stop()
