import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math

# ---------- Button Class ----------
# This class helps me manage each calculator button: how it looks, how it reacts to hand hover and click
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        self.isHovered = False  # I use this to visually show if my finger is over a button

    def draw(self, img):
        # Change color when my finger hovers over a button
        color_fill = (255, 255, 255) if self.isHovered else (225, 225, 225)
        color_border = (0, 100, 255) if self.isHovered else (50, 50, 50)

        # Draw the button rectangle
        cv2.rectangle(img, self.pos,
                      (self.pos[0] + self.width, self.pos[1] + self.height),
                      color_fill, cv2.FILLED)
        cv2.rectangle(img, self.pos,
                      (self.pos[0] + self.width, self.pos[1] + self.height),
                      color_border, 3)
        # Draw the button label
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    def checkHover(self, x, y):
        # I check if my finger is inside the button area
        self.isHovered = self.pos[0] < x < self.pos[0] + self.width and \
                         self.pos[1] < y < self.pos[1] + self.height
        return self.isHovered

    def checkClick(self, x, y):
        # I confirm a click if my finger hovers AND pinches
        return self.checkHover(x, y)

# ---------- Calculator Button Layout ----------
# Here I add all the calculator buttons
button_values = [
    ['7', '8', '9', '*', 'sqr'],
    ['4', '5', '6', '-', '^2'],
    ['1', '2', '3', '+', 'C'],
    ['0', '/', '.', '=', 'CC']
]

buttons = []
for y, row in enumerate(button_values):
    for x, val in enumerate(row):
        xpos = x * 100 + 100
        ypos = y * 100 + 140
        buttons.append(Button((xpos, ypos), 100, 100, val))

# ---------- Variables ----------
equation = ""  # I use this to store the current input expression
delay_counter = 0  # This helps avoid multiple clicks from one gesture

# ---------- Webcam Setup ----------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set webcam width
cap.set(4, 760)   # Set webcam height
detector = HandDetector(detectionCon=0.8, maxHands=1)  # Initialize hand detector

# ---------- Main App Loop ----------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image so it's like a mirror
    hands, img = detector.findHands(img)

    # Draw calculator display screen
    cv2.rectangle(img, (50, 50), (650, 130), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (50, 50), (650, 130), (50, 50, 50), 3)

    # Show all buttons
    for button in buttons:
        button.draw(img)

    # Show the current input/equation on the screen
    cv2.putText(img, equation, (60, 120), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 0, 0), 3)

    # If my hand is detected
    if hands:
        lmList = hands[0]["lmList"]
        x1, y1 = lmList[8][0], lmList[8][1]   # Tip of index finger
        x2, y2 = lmList[12][0], lmList[12][1] # Tip of middle finger

        # Calculate distance between fingers to detect a "click"
        length, _, img = detector.findDistance((x1, y1), (x2, y2), img)

        # Highlight buttons if I hover over them
        for button in buttons:
            button.checkHover(x1, y1)

        # If pinch gesture is detected (click)
        if length < 40 and delay_counter == 0:
            for button in buttons:
                if button.checkClick(x1, y1):
                    val = button.value

                    # Perform calculation or action
                    if val == "=":
                        try:
                            equation = str(eval(equation))  # Evaluate the math expression
                        except:
                            equation = "Error"  # Show error if evaluation fails
                    elif val == "CC":
                        equation = ""  # Clear all
                    elif val == "C":
                        equation = equation[:-1]  # Delete last character
                    elif val == "^2":
                        try:
                            equation = str(eval(equation) ** 2)  # Square the result
                        except:
                            equation = "Error"
                    elif val == "sqr":
                        try:
                            equation = str(math.sqrt(eval(equation)))  # Square root
                        except:
                            equation = "Error"
                    else:
                        equation += val  # Add the digit/operator to current equation
                    delay_counter = 1  # Start delay so it doesn’t re-click instantly

    # Delay logic to prevent multiple triggers from one gesture
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0

    # Show the app window
    cv2.imshow("Virtual Calculator", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break  # I can press 'q' to quit

# ---------- Clean up ----------
cap.release()
cv2.destroyAllWindows()


