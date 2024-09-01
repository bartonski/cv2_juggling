import cv2
import sys

filename = str(sys.argv[-1])

cap = cv2.VideoCapture(filename)

cv2.namedWindow("Juggling", cv2.WINDOW_NORMAL)

ret, frame = cap.read()

while ret:
    cv2.imshow("Juggling", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

