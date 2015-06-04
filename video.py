import numpy as np
import cv2

cap = cv2.VideoCapture(0)

HueDis = np.zeros((8, 360, 360), dtype = np.int)
for id in xrange(0, 7):
    for i in xrange(0, 359):
        for j in xrange(0, 359):
            HueDis[id][i][j] = computeArcDistance(i, j, id);
while(True):
    # Capture frame-by-frame
    ret, frame_rgb = cap.read()

    frame_rgb_float = frame_rgb.astype('float32')
    frame_hsv = cv2.cvtColor(frame_rgb_float, cv2.COLOR_BGR2HSV)
    H = frame_hsv[:, :, 0]
    print np.max(H), np.min(H)





    cv2.imshow('frame',frame_rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

def computeArcDistance(int i,int j,int id):
    int dis = 0
    if (region1Arcs[id] != 0):
        int border1 = (arc - region1Arcs[id]/2 + 360 ) % 360
        
