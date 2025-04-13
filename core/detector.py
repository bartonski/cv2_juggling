import sys
import cv2
import pdb
import math

class Detector:
    """ This class provides a tree representation of the functions
        call stack. If a function has no parent in the kernel (interrupt,
        syscall, kernel thread...) then it is attached to a virtual parent
        called ROOT.
    """

    def __init__(self, config):
        self._history = config['detector_history']
        self._threshold = config['detector_threshold']
        self._grey_threshold_max = config['grey_threshold']
        self._grey_threshold_min = config['grey_threshold'] - 1
        self._area_threshold = config['area_threshold']
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

    def contours( self, mask ):
        contours, _ = cv2.findContours( mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )
        self.detected_contours = contours
        return contours

    def centers( self ):
        centers = []
        for contour in self.contours:
            area = cv2.contourArea(contour)
            if area > self._area_threshold:
                M = cv2.moments(contour)
                centers.append( [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ] )
        return centers

class Tracker:
    def __init__(self, config):
        self._travelers = []
        self._unchecked_travelers = []
        self._traveler_history_depth = config['traveler_history_depth']
        self._area_threshold = config['area_threshold']
        self._tracking_threshold = config['tracking_threshold']
        self._traveler_id = 0

    def get_traveler_id( self ):
        self._traveler_id += 1
        return self._traveler_id


    def get_center( self, contour ):
        M = cv2.moments(contour)
        return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]

    def new_traveler(self, contour, area):
        traveler = {
            "center": self.get_center(contour),
            "seen": False,
            "contour": contour,
            "area": area
        }
        return traveler

    def velocity_and_distance(self, current_traveler, old_traveler):
        velocity_x = current_traveler["center"][0] - old_traveler["center"][0]
        velocity_y = current_traveler["center"][1] - old_traveler["center"][1]
        return {
            "velocity": [velocity_x, velocity_y],
            "distance":math.hypot(velocity_x, velocity_y)
        }

    def populate_traveler(self, new, old, velocity):
        new_velocity = velocity
        old_velocity = None
        if old.get("velocity"):
            old_velocity = old["velocity"]
            if old["seen"]:
                acceleration_x = new_velocity[0] - old_velocity[0]
                acceleration_y = new_velocity[1] - old_velocity[1]
                new["acceleration"] = [ acceleration_x, acceleration_y]
        if old.get("traveler_id"):
            new["traveler_id"] = old["traveler_id"]
        else:
            new["traveler_id"] = self.get_traveler_id()
        new["seen"] = True,

        return new

    def read_frame(self, contours):
        checked_travelers = []
        traveler = {}
        for contour in contours:
            area = cv2.contourArea(contour)
            #print(f"{area}")
            current_travelers = []
            if area > self._area_threshold:
                traveler = self.new_traveler( contour, area )
                for unchecked_traveler in self._unchecked_travelers:
                    vad = self.velocity_and_distance( traveler, unchecked_traveler)
                    if vad["velocity"]:
                        velocity = vad["velocity"]
                    if vad["distance"] <= self._tracking_threshold:
                        traveler = self.populate_traveler(
                            traveler, unchecked_traveler, velocity)
                        checked_travelers.append( unchecked_traveler )
                current_travelers.append( traveler )
        self._unchecked_travelers = current_travelers;
        # pdb.set_trace()
        self._travelers.append(checked_travelers)
        if len(self._travelers) > self._traveler_history_depth:
            self._travelers.pop(0)

def main():
    detector_config = {
        'detector_history': 100,
        'detector_threshold': 20,
        'area_threshold': 50,
        'grey_threshold': 255
    }
    tracker_config = {
        'traveler_history_depth': 3,
        'area_threshold': 50,
        'tracking_threshold': 30
    }
    filename = str(sys.argv[-1])

    cap = cv2.VideoCapture(filename)

    jd = Detector( detector_config )
    tracker = Tracker( tracker_config )

    cv2.namedWindow("Juggling")
    cv2.namedWindow("Mask")

    ret, frame = cap.read()
    # ret = True
    count = 0
    while ret:
        # Get layers
        mask = jd.mask( frame )
        print( f"Count: {count}")
        count += 1
        contours = jd.contours( mask )
        tracker.read_frame(contours)
        cv2.imshow("Juggling", frame)
        cv2.imshow("Mask", mask)
        #pdb.set_trace()

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
