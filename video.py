#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import time
import struct

# constant
width = 640 #1280/3
height = 360 #720/3

cap = cv2.VideoCapture(0)

# calculate frame rate
dt = time.time()
count = 0

# RGB frame -> H,S string
def to_HS_data(frame_rgb):
    size = frame_rgb.shape[0] * frame_rgb.shape[1]
    global weight, height
    assert size == width*height
    frame_rgb_float = frame_rgb.astype('float32')
    frame_hsv_float = cv2.cvtColor(frame_rgb_float, cv2.COLOR_BGR2HSV)
    H = frame_hsv_float[:, :, 0].astype('uint16').reshape((size))
    S = (frame_hsv_float[:, :, 1] * 255).astype('uint8').reshape((size))
    return (H.tostring() + S.tostring(), frame_hsv_float)

# H string + HSV float -> RGB frame
def from_H_data(frame_hsv_float, H):
    H = np.fromstring(H, dtype = 'uint16').astype('float32').reshape((height, width))
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
    frame_rgb = frame_rgb_original[::2, ::2, :]
    assert frame_rgb.shape == (height, width, 3)

    # send
    data_send, frame_hsv_float = to_HS_data(frame_rgb.copy())
    assert len(data_send) == height*width*3
    p.stdin.write(data_send)

    # receive
    data_recv = p.stdout.read(height*width*2 + 8)
    assert len(data_recv) == height*width*2 + 8
    frame_rgb_new = from_H_data(frame_hsv_float, data_recv[:height*width*2])

    # template id, arc
    print '(template ID, arc) = ',
    print struct.unpack('<ll', data_recv[-8:])

    # combine old and new
    frame_rgb_new = np.concatenate((frame_rgb, frame_rgb_new), axis = 0)

    # show
    cv2.imshow('frame',frame_rgb_new)

    # print frame rate
    count += 1
    print "%.1f fps" % (float(count) / (time.time() - dt))
    print ''

    # intterupt -> end
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
