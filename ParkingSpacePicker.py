import cv2
import pickle

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

temp = []
counter = 0

def mouseClick(events, x, y, flag, params):
    global counter
    if events == cv2.EVENT_LBUTTONDOWN:
        temp.append((x, y))
        cv2.circle(img, (x, y), 3, (255, 0, 0), cv2.FILLED)
        counter = counter + 1

        if counter % 4 == 0:
            posList.append(temp.copy())
            with open('CarParkPos', 'wb') as f:
                pickle.dump(posList, f)
            temp.clear()


while True:
    img = cv2.imread('cam2pic.png')

    for pos in posList:
        for i in range(0, 4):
             x, y = pos[i]
             pt1, pt2, pt3, pt4 = pos[0], pos[1], pos[2], pos[3]
             cv2.circle(img, (x, y), 3, (255, 0, 0), cv2.FILLED)

        cv2.line(img, (pt1), (pt2), (0, 255, 0), 3)
        cv2.line(img, (pt2), (pt4), (0, 255, 0), 3)
        cv2.line(img, (pt4), (pt3), (0, 255, 0), 3)
        cv2.line(img, (pt3), (pt1), (0, 255, 0), 3)


    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
