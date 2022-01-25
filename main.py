import cv2
import cvzone
import numpy as np
import pickle

# video feed
cap = cv2.VideoCapture('cam2.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

punny = np.array(posList)

def checkParkingSpace(imgPro):
    width, height = 107, 48
    spaceCounter = 0

    for pos in posList:           # used to draw lines and circles
        for i in range(0, 4):
             x, y = pos[i]
             #print((x,y))
             pt1, pt2, pt3, pt4 = pos[0], pos[1], pos[2], pos[3]
             cv2.circle(img, (x, y), 3, (255, 0, 0), cv2.FILLED)

        pts1 = np.float32([pt1, pt2, pt3, pt4])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOutput = cv2.warpPerspective(imgPro, matrix, (width, height))
        #cv2.imshow(str(x*y), imgOutput)

        count = cv2.countNonZero(imgOutput)
        cvzone.putTextRect(img, str(count), (x-width, y), scale=1, thickness=2, offset=0)

        if count<900:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2

        cv2.line(img, (pt1), (pt2), color, 3)
        cv2.line(img, (pt2), (pt4), color, 3)
        cv2.line(img, (pt4), (pt3), color, 3)
        cv2.line(img, (pt3), (pt1), color, 3)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=3, offset=20, colorR=(0,200,0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernal = np.ones((3, 3), np.uint8)
    imgDilates = cv2.dilate(imgMedian, kernal, iterations=1)
   # cv2.imshow("dilimg", imgDilates)

    checkParkingSpace(imgDilates)
    cv2.imshow("Image", img)
    cv2.waitKey(10)

