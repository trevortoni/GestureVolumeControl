# This script enables the webcam
# This module gets the position of the hand landmarks for the user easily
import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        # Create an object called hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionConf, self.trackConf)
        # for connecting all the hand points detected
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            # extract the information for each hand that is detected
            for handLms in self.results.multi_hand_landmarks:
                # for a single hand
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        # list with all the landmarks positions
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                height, width, c = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    # if id == 4:  # for choosing which landmark gets highlighted
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        # add the argument draw=False in the two functions below in order to disable drawing
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            # gets the landmark no specified and prints it if the list has something
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


if __name__ == "__main__":
    main()
