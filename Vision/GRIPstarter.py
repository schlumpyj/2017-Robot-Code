import cv2 as cv
import numpy as np
import grip
from GRIPget import WebcamVideoStream
import time
from RPILed import leds
leds = leds().start()
vid1 = WebcamVideoStream(src=0).start()
another = grip.GripPipeline()
counter = 0
start = time.time()
try:
    while True:
        img1 = vid1.read()
        another.process(img1)
        counter+=1
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
except KeyboardInterrupt:
    print (counter/(time.time()-start))
    vid1.release()
    leds.stop()
