import cv2

import numpy as np

import HandTrackingModule as htm

import time
import pyautogui
###############################################
wCam,hCam=640,480
frameR=100
smoothening =7
###############################################
pTime=0
plocX,plocY=0,0
clocX,clocY=0,0
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector =htm.HandDetector(maxHands=1)
wScr,hScr=pyautogui.size()
while True:
    success,img=cap.read()
    img= detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
    fingers=detector.fingersUp()

    if len(fingers)>=3:
        if fingers[1] ==1 and fingers[2]==0:
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            clocX=plocX +(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            pyautogui.moveTo(wScr-clocX,clocY)
            plocX,plocY=clocX,clocY

    if len(fingers)>=3 and fingers[1]==1 and fingers[2]==1:
        length,img,linelnfo =detector.findDistance(8,12,img)
        if length<40:
            pyautogui.click()
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f"FPS:{int(fps)}",(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("image",img)
    cv2.waitKey(1)

