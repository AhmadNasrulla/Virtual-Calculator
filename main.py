import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# ---------------- Button Class ----------------
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        self.isHovered = False

    def draw(self, img):
        color_fill = (255, 255, 255) if self.isHovered else (225, 225, 225)
        color_border = (0, 100, 255) if self.isHovered else (50, 50, 50)

        cv2.rectangle(img, self.pos,
                      (self.pos[0] + self.width, self.pos[1] + self.height),
                      color_fill, cv2.FILLED)
        cv2.rectangle(img, self.pos,
                      (self.pos[0] + self.width, self.pos[1] + self.height),
                      color_border, 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    def checkHover(self, x, y):
        self.isHovered = self.pos[0] < x < self.pos[0] + self.width and \
                         self.pos[1] < y < self.pos[1] + self.height
        return self.isHovered

    def checkClick(self, x, y):
        return self.checkHover(x, y)

# ---------------- Calculator Setup ----------------
button_values = [['7', '8', '9', '*'],
                 ['4', '5', '6', '-'],
                 ['1', '2', '3', '+', 'C'],
                 ['0', '/', '.', '=', 'CC'],
                ]

buttons = []
for y, row in enumerate(button_values):
    for x, val in enumerate(row):
        xpos = x * 100 + 50
        ypos = y * 100 + 150
        buttons.append(Button((xpos, ypos), 100, 100, val))

# ---------------- Variables ----------------
equation = ""
delay_counter = 0

# ---------------- Webcam Setup ----------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

# ---------------- Main Loop ----------------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Draw calculator display panel
    cv2.rectangle(img, (50, 50), (650, 130), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (50, 50), (650, 130), (50, 50, 50), 3)

    # Draw buttons
    for button in buttons:
        button.draw(img)

    # Display current equation
    cv2.putText(img, equation, (60, 120), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 0, 0), 3)

    # Check for hand & gesture
    if hands:
        lmList = hands[0]["lmList"]
        x1, y1 = lmList[8][0], lmList[8][1]   
        x2, y2 = lmList[12][0], lmList[12][1]

        length, _, img = detector.findDistance((x1, y1), (x2, y2), img)

        # Update hover effect
        for button in buttons:
            button.checkHover(x1, y1)

        # Detect click (pinch gesture)
        if length < 40 and delay_counter == 0:
            for button in buttons:
                if button.checkClick(x1, y1):
                    val = button.value
                    if val == "=":
                        try:
                            equation = str(eval(equation))
                        except:
                            equation = "Error"
                    elif val == "CC":
                        equation = ""
                    elif val == "C":
                        equation = equation[:-1]
                    else:
                        equation += val
                    delay_counter = 1

    # Click delay logic
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0

    # Display
    cv2.imshow("Virtual Calculator", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
