import sys
import cv2

config = []
config["cv2"] = cv2

filename = str(sys.argv[-1])

cap = cv2.VideoCapture(filename)

cv2.namedWindow("Juggling", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

#ret, frame = cap.read()
ret = True

while ret:
    ret, frame = cap.read()

    # Get layers
    cv2.imshow("Juggling", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()

