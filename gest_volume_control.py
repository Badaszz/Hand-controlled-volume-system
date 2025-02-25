import cv2
import mediapipe as mp
import hand_tracking_module2 as htm
import numpy as np
import time
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#####################
wCam, hCam = 240,240
#####################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
cTime = 0

detector = htm.handDetector(detectionConfd = 0.7) #a higher confidence s required for detection

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volume.GetVolumeRange()

# Volume Range is (-65.25, 0.0, 0.75) 0 is highest and -65.25 is lowest
#volume.SetMasterVolumeLevel(-20.0, None)
volume_range = volume.GetVolumeRange()
minVol = volume_range[0]
maxVol = volume_range[1]
vol=0
vol_for_bar = 100

while True:
    success, img = cap.read()
    img = detector.findLandmarks(img, draw=False)
    lmlist = detector.findLmPositions(img)
    if len(lmlist) != 0: 
        #print(lmlist[4], lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2] #x,y point for the tip of the thumb landmark
        x2,y2 = lmlist[8][1],lmlist[8][2] #x,y point for the tip of the index finger
        cx,cy = (x1+x2)//2, (y1+y2)//2 #center point between the thumb and index finger
        
        cv2.circle(img, (x1,y1), 7, (0,255,0),cv2.FILLED)
        cv2.circle(img, (x2,y2), 7, (0,255,0),cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)
        cv2.circle(img, (cx,cy), 3, (0,255,0),cv2.FILLED) #center point
        length = math.hypot(x2-x1, y2-y1) #distance between the thumb and index finger
        #print(length) #print the distance between the thumb and index finger
        #Hand range is 25 to 100
        #Volume range is -65.25 to 0
        vol = np.interp(length, [25, 100], [minVol, maxVol])
        vol_for_bar = np.interp(length, [25, 100], [100, 200])
        #vol_percent = np.interp(length, [25, 100], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        
    cv2.rectangle(img, (25,100), (40,200), (0,255,0), 2) 
    cv2.rectangle(img, (25,int(vol_for_bar)), (40,200), (0,255,0), cv2.FILLED)
    
    img2 = cv2.flip(img,1)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img2, f'FPS: {int(fps)}', (10,25), cv2.FONT_ITALIC, 1, (0,0,255), 1)
    cv2.imshow("VIDEO FEED BROSKI", img2)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break