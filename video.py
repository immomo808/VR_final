#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

# calculate frame rate
dt = time.time()
count = 0

# RGB frame -> H,S string
def to_HS_data(frame_rgb):
    size = frame_rgb.shape[0] * frame_rgb.shape[1]
    frame_rgb_float = frame_rgb.astype('float32')
    frame_hsv_float = cv2.cvtColor(frame_rgb_float, cv2.COLOR_BGR2HSV)
    H = frame_hsv_float[:, :, 0].astype('uint16').reshape((size))
    S = (frame_hsv_float[:, :, 1] * 255).astype('uint8').reshape((size))
    return (H.tostring() + S.tostring(), frame_hsv_float)

# H string + HSV float -> RGB frame
def from_H_data(frame_hsv_float, H):
    H = np.fromstring(H, dtype = 'uint16').astype('float32').reshape((180, 320))
    frame_hsv_float[:, :, 0] = H
    frame_rgb_float = cv2.cvtColor(frame_hsv_float, cv2.COLOR_HSV2BGR)
    frame_rgb = frame_rgb_float.astype('uint8')
    return frame_rgb


import subprocess
args = ['./frame_processor']
p = subprocess.Popen(args, stdout = subprocess.PIPE, stdin = subprocess.PIPE)

while(True):
    # Capture frame-by-frame
    ret, frame_rgb_original = cap.read()

    # resize
    frame_rgb = frame_rgb_original[::4, ::4, :]

    # send
    data_send, frame_hsv_float = to_HS_data(frame_rgb)
    p.stdin.write(data_send)

    # receive
    data_recv = p.stdout.read(57600*2)
    frame_rgb = from_H_data(frame_hsv_float, data_recv)

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
