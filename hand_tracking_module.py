#hand tracking module

import cv2
import mediapipe as mp
import time

#create the Hand detector class
class handDetector():
    #initialization parametrs and defaults
    def __init__(self, mode = False, maxHands = 2, detectionConfd = 0.5,trackConfd = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfd = detectionConfd
        self.trackConfd = trackConfd
        self.mpHands = mp.solutions.hands
        #declaring the mphands 
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConfd,
            min_tracking_confidence=self.trackConfd
        )
        #the mphands drawings class
        self.mpDraw = mp.solutions.drawing_utils
        #self.mpConnect = self.mpHands.HAND_CONNECTIONS()
    #defining the findlandmarks method
    def findLandmarks(self,img, draw = True):
        #convert image to RGB format which mediapipe can work with
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #process the image with mpHands to find hand landmarks
        self.results = self.hands.process(imgRGB)
        #check if landmarks are detected
        if self.results.multi_hand_landmarks:
            #loop through the hands present
            for handlms in self.results.multi_hand_landmarks:
                #only draw when draw = True in the method
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img
    #define find landmark positions method
    def findLmPositions(self, img, draw = False, lmk = 4):
        lmpositions = []
        if self.results.multi_hand_landmarks:
            #detected hands
            det_hands = self.results.multi_hand_landmarks
            Hand_Num=0
            for handlms in det_hands:
                for Id,lm in enumerate(handlms.landmark):
                    #get the shape of the image
                    h, w, c = img.shape
                    #compute the pixel points of the landmarks
                    cx,cy = int(lm.x*w), int(lm.y*h) #x is the ratio of the width of the image and y is the ratio of the height of the image
                    lmpositions.append([Hand_Num,Id,cx,cy])
                    if draw:
                        if Id == lmk:
                            #draw a circle around a particular landmark
                            cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
                Hand_Num+=1
        return lmpositions      

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findLandmarks(img)
        handLists = detector.findLmPositions(img, draw = False)
        #TO get the frames per second
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        for i in handLists:
            if i[0] == 0:
                if i[1] ==4:
                    cv2.circle(img, (i[2],i[3]), 15, (0,0,255), cv2.FILLED)
        #flip image
        img2 = cv2.flip(img, 1)
        #display frames per second
        cv2.putText(img2, str(int(fps)), (10,70), cv2.FONT_ITALIC, 2, (0,0,255), 2)
        #image display
        cv2.imshow("video feed broski", img2)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break 


if __name__ == "__main__":
    main()