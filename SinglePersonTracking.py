import math
import time
from datetime import datetime

import cv2
import mediapipe as mp


class poseDetector():

    #Instaniating variables
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        self.pose = self.mpPose.Pose(self.mode
                                     , min_detection_confidence=0.5
                                     , min_tracking_confidence=0.5
                                     )

    #Finds pose of person
    def findPose(self, img, draw=True, nodes_only=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    #Superimposes the nodes in something
    def superimpose(
            self,
            img,
            bg,
            node_color=(200, 200, 0),
            node_size=5,
            connector_color=(170, 150, 0),
            connector_thickness=5
    ):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            self.mpDraw.draw_landmarks(bg, self.results.pose_landmarks,
                                       self.mpPose.POSE_CONNECTIONS,
                                       self.mpDraw.DrawingSpec(color=node_color, thickness=2, circle_radius=node_size),
                                       self.mpDraw.DrawingSpec(color=connector_color, thickness=5, circle_radius=connector_thickness))
        return img

    #Finds position of person
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = round(lm.x, 3), round(lm.y, 3)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    #Finds angle between three different nodes
    def findAngle(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle = angle + 360

        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle


def main(fileAddress):
    # cap = cv2.VideoCapture(0) # - overloaded

    cap = cv2.VideoCapture(fileAddress)

    # get the duration in seconds
    # frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # try:
    #     duration = round(frames / fps)
    # except ZeroDivisionError:
    #     pass
    # video_time = datetime.timedelta(seconds=duration)

    # pTime = 0
    # start_time = time.time()

    detector = poseDetector()

    absList = []

    while True:
        # seconds_passed = time.time() - start_time
        # if seconds_passed > duration:
        #     break

        success, img = cap.read()
        if not success:
            break

        # img = ~img
        img = cv2.flip(img, 1)
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        absList.append(lmList)

        # print coordinates
        for i in range(len(lmList)):
            print(lmList[i])

        # if len(lmList) != 0:
        # print(lmList[14])
        # cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        # cTime = time.time()
        # fps = 1 / (cTime - pTime)
        # pTime = cTime

        # cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
        #           (255, 0, 0), 3)

        img = cv2.flip(img, 1)

        cv2.putText(img, "Dance Pose Analysis:", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # cv2.waitKey(0)
        # break

    return absList


# if __name__ == "__main__":
#     main()


def calcAngle(f, absList, n1, n2, n3):
    # Get the landmarks
    y3 = absList[f][n3][2]
    y2 = absList[f][n2][2]
    y1 = absList[f][n1][2]

    x3 = absList[f][n3][1]
    x2 = absList[f][n2][1]
    x1 = absList[f][n1][1]

    # Calculate the angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

    if angle < 0:
        angle = abs(angle)

    return angle


def createAngleList(absList):
    jointNodes = [[13, 11, 23], [15, 13, 11], [14, 12, 24], [16, 14, 12], [11, 23, 25], [23, 25, 27], [25, 27, 31],
                  [12, 24, 26], [24, 26, 28], [24, 26, 28], [26, 28, 32]]

    angleList = []

    for i in range(len(absList)):

        subList = []

        # for each frame: 
        for j in range(10):
            a, b, c = jointNodes[j][0], jointNodes[j][1], jointNodes[j][2]
            angle = calcAngle(i, absList, a, b, c)
            subList.append(round(angle, 3))

        angleList.append(subList)

    return angleList


def getAngleList(fileAddress):
    absList = main(fileAddress)
    print('Debug: Done With GetAngleList!!')
    print('\n\n\n Printing AbsList!! --------------')
    print(absList)
    return createAngleList(absList)

# print('\n\n\nFinal Print!!')
# print(getAngleList("./Assets/Q9J9xyGC.mov"))
