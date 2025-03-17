import cv2
import sys
from core.detector import Detector

def main():
    detector_config = {
        'detector_history': 100,
        'detector_threshold': 40,
        'grey_threshold': 255
    }
    filename = str(sys.argv[-1])

    cap = cv2.VideoCapture(filename)

    jd = Detector( detector_config ) 

    cv2.namedWindow("Juggling")
    cv2.namedWindow("Mask")

    ret, frame = cap.read()
    # ret = True

    while ret:
        # Get layers
        mask = jd.mask( frame )
        cv2.imshow("Juggling", frame)
        cv2.imshow("Mask", mask) 

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
