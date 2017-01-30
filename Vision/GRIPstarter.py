import cv2 as cv
import numpy as np
import grip
import time
vid1 = cv.VideoCapture(0)
another = grip.GripPipeline()
counter = 0
start = time.time()
try:
    while True:
        _, img1 = vid1.read()
        another.process(img1)
        counter+=1
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
except:
    print (counter/(time.time()-start))
    vid1.release()
    cv.destroyAllWindows()
