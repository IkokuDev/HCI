import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
#autopy, a module used to gain control of the trackpad, refused to install
#FIX: had to downgrade pip installer to version 20

##############
wCam, hCam = 640, 480
frameReduction = 100 #border in which mouse movements are valid || essentially a trackpad
smoothening = 7
##############
pTime = 0
pLocX, pLocY = 0,0
cLocX, cLocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
#an opencv method used to get video from the webcam
#here it is set to 0 in order to use the primary webcam. other values can be used.
#set method used for fixed window size( 3 and 4 are prop IDs for width and height respectively)
#variables pTime and cTime represent previous time and current time respectively, and used later to calculate
#the frame rate in fps
#HandDetector class from HandTracking module is initialised with an object called detector
#a method from autopy helps to get the exact width and height of the screen. This is used later to
#convert the movements of the finger to match mouse movement

while True:
    #1. get hand landmarks as per opencv documentation
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #2. access tip of tracking finger and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #x1 and y1 for index finger, x2 and y2 for middle finger. coordinates provided by opencv documentation

        #3. how to check which fingers are up. METHOD ALREADY IMPLEMENTED IN MODULE
        fingers = detector.fingersUp()
        #frame reduction border for movement effective range
        cv2.rectangle(img, (frameReduction, frameReduction), (wCam - frameReduction, hCam - frameReduction),
                          (255, 255, 0), 2)

        #4. index finger: tracking mode. index fingertip is 1st element, middle fingertip is 2nd, thumb=0
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. convert landmark coordinates using numpy interp()
            x3 = np.interp(x1, (frameReduction, wCam - frameReduction), (0,wScr))
            y3 = np.interp(y1, (frameReduction, hCam - frameReduction), (0, hScr))
            #6.  smoothen the values
            cLocX = pLocX + (x3 - pLocX)/smoothening
            cLocY = pLocY + (y3 - pLocY)/smoothening
            #7. move mouse
            autopy.mouse.move(wScr - cLocX, cLocY)
            #BUG: movement on x-axis was inverted. FIX: subtract xcoordinates from screen width
            cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
            pLocX, pLocY = cLocX, cLocY
        #8. both index finger and middle finger = clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            #9. find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            #10. click mouse if distance is short
            if length < 35:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 8, (0, 255, 0), cv2.FILLED) #turn center circle green
                autopy.mouse.click() #initiate click





    #11. frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    #12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)




