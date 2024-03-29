# This script enables the webcam
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
# Create an object called hands
hands = mpHands.Hands()
# for connecting all the hand points detected
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    # the presence of hands
    if results.multi_hand_landmarks:
        # extract the information for each hand that is detected
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                print(id, cx, cy)

                if id == 4: # for choosing which landmark gets highlighted
                  cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)


            # for a single hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
