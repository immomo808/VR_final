#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

# calculate frame rate
dt = time.time()
count = 0


# input ：(???, ???, 3) uint8 RGB
# ouptut：(360) int
def H_histogram(frame_rgb):
    size = frame_rgb.shape[0] * frame_rgb.shape[1]
    frame_rgb_float = frame_rgb.astype('float32')
    frame_hsv_float = cv2.cvtColor(frame_rgb_float, cv2.COLOR_BGR2HSV)
    H = frame_hsv_float[:, :, 0].astype('int').reshape((size))
    S = (frame_hsv_float[:, :, 1] * 255).astype('int').reshape((size))
    H_bin = np.zeros((360), 'int')
    for i in range(size):
        H_bin[H[i]] += S[i]
    return H_bin


while(True):
    # Capture frame-by-frame
    ret, frame_rgb_original = cap.read()

    # resize
    frame_rgb = frame_rgb_original[::4, ::4, :]

    # H histogram
    H_bin = H_histogram(frame_rgb)

    # show
    cv2.imshow('frame',frame_rgb)

    # print frame rate
    count += 1
    print "%.1f fps" % (float(count) / (time.time() - dt))

    # intterupt -> end
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
