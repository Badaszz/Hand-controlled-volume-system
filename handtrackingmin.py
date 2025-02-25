#code to track hands

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
cap.set(3, 240)
cap.set(4, 240)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mpConnect = mpHands.HAND_CONNECTIONS

pTime = 0
cTime = 0
while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
       for handlms in results.multi_hand_landmarks:
            for Id,lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h) #x is the ratio of the width of the image and y is the ratio of the height of the image
                if Id == 8:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
                    #draw a circle around a landmark 
                #print(Id,cx,cy) #printing the x,y points for each landmark
            #mpDraw.draw_landmarks(img, handlms, mpConnect)

    #TO get the frames per second
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    img2 = cv2.flip(img, 1)
    cv2.putText(img2, str(int(fps)), (10,70), cv2.FONT_ITALIC, 2, (0,0,255), 2)
    cv2.imshow("video feed broski", img2)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break 
