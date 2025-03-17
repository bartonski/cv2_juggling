import sys
import cv2


class JugglingObjectDetector:
    """ This class provides a tree representation of the functions
        call stack. If a function has no parent in the kernel (interrupt,
        syscall, kernel thread...) then it is attached to a virtual parent
        called ROOT.
    """
    ROOT = None

    def __init__(self, config):
        self._history = config['detector_history']
        self._threshold = config['detector_threshold']
        self._grey_threshold_max = config['grey_threshold']
        self._grey_threshold_min = config['grey_threshold'] - 1
        self.object_detector = cv2.createBackgroundSubtractorMOG2(
                                   history=self._history,
                                   varThreshold=self._threshold )

    def mask( self, mask_input ):
        mask = self.object_detector.apply( mask_input )
        _, mask = cv2.threshold( mask,
                                 self._grey_threshold_min,
                                 self._grey_threshold_max,
                                 cv2.THRESH_BINARY )
        return mask
        


def main():
    config = {
        'detector_history': 100,
        'detector_threshold': 40,
        'grey_threshold': 255
    }
    filename = str(sys.argv[-1])

    cap = cv2.VideoCapture(filename)

    jd = JugglingObjectDetector( config ) 

    cv2.namedWindow("Juggling", cv2.WINDOW_NORMAL)
    #cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

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
