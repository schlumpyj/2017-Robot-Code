#!/usr/bin/python

"""
This file is for the Raspberry Pi LED control

Currently, there are these modes programmed:

- While gear is in, it is red
- If no gear, mecanum is down == Green
- If no gear, tank is down == Pink or Purple
- If not enabled, cycle through colors


TODO:
- Load on boot
- Add time.sleep so we don't use so much CPU
- Add Auto Color maybe
"""

from networktables import NetworkTable
import pigpio
import time
import colorsys
import sys

class RPIled(object):

	RED_PIN   = 22
	GREEN_PIN = 17
	BLUE_PIN  = 24

	def __init__(self):

		self.pi = pigpio.pi()
		NetworkTable.initialize(server='10.44.80.2')
		self.table = NetworkTable.getTable('SmartDashboard')
		self.isUp = "mecanum"
		self.isGear = "nope"
		self.isEnabled = False
		self.cancel = False

	def setLights(self, pin, brightness):
		realBrightness = int(int(brightness) * (float(255) / 255.0))
		self.pi.set_PWM_dutycycle(pin, realBrightness)

	def start(self):

		Thread(target=self.update, args=()).start()
		return self

	def ledGo(self):
		counter = 0
		while not self.cancel:
			try:
	            isUp = table.getString("State", "mecanum")
	            isGear = table.getString("Gear", "nope")
	            isEnabled = table.getBoolean("enabled", False)
	        except KeyError:
	            print "KeyError"

		    if isEnabled:

		        if isGear == "yep":
		            self.setLights(RED_PIN, 0)
		            self.setLights(BLUE_PIN, 0)
		            self.setLights(GREEN_PIN, 255)

		        else:

		            if isUp == "mecanum":

		                self.setLights(RED_PIN, 0)
		                self.setLights(BLUE_PIN, 0)
		                self.setLights(GREEN_PIN, 255)

		            else:

		                self.setLights(RED_PIN, 255)
		                self.setLights(BLUE_PIN, 255)
		                self.setLights(GREEN_PIN, 0)
		    else:
		        counter+=.00005
		        if counter > 1.00:
		            counter = 0
		        output = colorsys.hsv_to_rgb(counter, 1, 1)
		        self.setLights(RED_PIN, (output[0]*255))
		        self.setLights(GREEN_PIN, (output[1]*255))
		        self.setLights(BLUE_PIN, (output[2]*255))

		time.sleep(.05) #We will see if that effects anything

	def stop(self):

		self.cancel = True
		self.setLights(RED_PIN, 0)
		self.setLights(GREEN_PIN, 0)
		self.setLights(BLUE_PIN, 0)
		self.pi.stop()
		sys.exit()
