from collections import deque  # import deque a far faster list
import numpy as np  # import numpy as needed
import imutils  # we definately need imutils convienience functions.
import time  # time is time
import cv2  # The major library, opencv
import pyautogui

# define the lower boundary of the colour of the object in HSV
lower_color_boundary = (110, 50, 50)
# define the upper region of the colour of the object in HSV
upper_color_boundary = (130, 255, 255)


def gameControllerFunction(topLeft, centerLeft, bottomLeft, topCenter, middle, bottomCenter, topRight, centerRight, bottomRight):

    print("Booting the Video stream,")
    vs = cv2.VideoCapture(1)  # start the video stream.
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)  # create the 'frame' window
    time.sleep(2.0)  # set sleep time to 2.0 seconds

    if topCenter == None:
        # top center will be arrow key up
        topCenter = "up"
    if topLeft == None:
        # top left will be arrow key left
        topLeft = "left"
    if topRight == None:
        # top right will be arrow key right
        topRight = "right"
    if bottomCenter == None:
        # bottom center will be arrow key down
        bottomCenter = "down"

    while True:
        frame = vs.read()  # Read off the frame from the video stream
        ret, frame = frame  # Use this if you want to load in your video
        output = "None"
        key = None

        if frame is None:  # If there is no frame, save my pc from going through any stress at all
            break
        # otherwise, if we have a frame, we proceed with the following code
        # so much easier than open cv, keeping aspect ratio intact
        frame = imutils.resize(frame, width=700)
        # i want the mirror view, it's very helpful especially if i'm streaming
        frame = cv2.flip(frame, 1)

        windowDetails = cv2.getWindowImageRect('frame')

        # print(windowDetails)
        totalWidth = windowDetails[2]
        totalHeight = windowDetails[3]
        verLine1 = {
            'start': (totalWidth//3, 0),
            'end': (totalWidth//3, totalHeight)
        }
        verLine2 = {
            'start': (totalWidth//3 * 2, 0),
            'end': (totalWidth//3 * 2, totalHeight)
        }
        horLine1 = {
            'start': (0, totalHeight//3),
            'end': (totalWidth, totalHeight//3)
        }
        horLine2 = {
            'start': (0, totalHeight//3 * 2),
            'end': (totalWidth, totalHeight//3 * 2)
        }

        # processing the frame
        # blurr helps to reduce high frequency noise, definately helps model
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        # convert my color to the HSV format
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Create a mask
        # mask other regions except colors in range of upper to lower (thresholding)
        mask = cv2.inRange(hsv, lower_color_boundary, upper_color_boundary)
        # Reduce noise caused by thresholding
        mask = cv2.erode(mask, None, iterations=2)
        # foreground the found object i.e futher reduce noise.
        mask = cv2.dilate(mask, None, iterations=2)

        contours = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # find contours
        # Grab the contours using imutils
        contours = imutils.grab_contours(contours)
        center = None  # center is initially set to none
        if len(contours) > 0:  # if the contours list is not empty proceed
            # select contour with maximum Area, most likely our object
            contour = max(contours, key=cv2.contourArea)
            # pick up co-ordinates for drawing a circle around the object
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            M = cv2.moments(contour)  # Extract moments from the contour.
            # Obtain the centre of mass of the object.
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:  # if we have a reasonable radius for the proposed object detected
                # Draw a circle to bound the Object
                cv2.circle(frame, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                # Draw a filled in dot at the centre of the circle
                cv2.circle(frame, center, 5, (0, 0, 225), -1)

        if center:
            if center[0] <= totalWidth//3:
                if center[1] <= totalHeight//3:
                    output = "Top Left"
                    key = topLeft
                elif center[1] >= totalHeight//3*2:
                    output = "Bottom Left"
                    key = bottomLeft
                else:
                    output = "Center Left"
                    key = centerLeft
            elif center[0] >= totalWidth//3*2:
                if center[1] <= totalHeight//3:
                    output = "Top Right"
                    key = topRight
                elif center[1] >= totalHeight//3*2:
                    output = "Bottom Right"
                    key = bottomRight
                else:
                    output = "Center Right"
                    key = centerRight
            else:
                if center[1] <= totalHeight//3:
                    output = "Top Center"
                    key = topCenter
                elif center[1] >= totalHeight//3*2:
                    output = "Bottom Center"
                    key = bottomCenter
                else:
                    output = "Center"
                    key = middle

        if key:
            key_arr = key.split('+')

            # Key Presses
            for k in key_arr:
                pyautogui.keyDown(k.strip())

            time.sleep(0.08)

            for k in key_arr:
                pyautogui.keyUp(k.strip())

        # Drawing the grid
        cv2.putText(frame,  output,  (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 0, 0),  2,  cv2.LINE_4)

        cv2.line(frame, verLine1['start'], verLine1['end'], (255, 255, 255), 5)
        cv2.line(frame, verLine2['start'], verLine2['end'], (255, 255, 255), 5)
        cv2.line(frame, horLine1['start'], horLine1['end'], (255, 255, 255), 5)
        cv2.line(frame, horLine2['start'], horLine2['end'], (255, 255, 255), 5)
        cv2.imshow("frame", frame)  # let's see the frame X frame

        # Closing a video frame
        key = cv2.waitKey(1)  # wait for the cv key
        if key == ord("q"):  # If the x button is pressed
            break  # Break from the loop

    vs.release()  # Let opencv release the video loader
    cv2.destroyAllWindows()  # Destroy all windows to close it


if __name__ == "__main__":
    gameControllerFunction('left', 'left', 'left', "up",None, "down", 'right', 'right', 'right')