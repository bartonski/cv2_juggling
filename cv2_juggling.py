import cv2
import sys
from core.detector import Detector
from core.orientation import Orientation
from layers.pose_detection.pose_detector import PoseDetector

def main():
    filename = str(sys.argv[-1])
    detector_config = {
        'detector_history': 100,
        'detector_threshold': 40,
        'grey_threshold': 255
    }
    pose_detector_config = {
        'model_asset_path': 'layers/pose_detection/pose_landmarker_heavy.task'
    }
    # should populate orientation_config, pass to Orientation

    cap = cv2.VideoCapture(filename)
    orientation = Orientation(filename)
    jd = Detector( detector_config ) 
    pose = PoseDetector( pose_detector_config )

    cv2.namedWindow("Juggling")
    cv2.namedWindow("Mask")

    ret, frame = cap.read()
    frame = orientation.correct_rotation(frame)
    
    # ret = True

    while ret:
        mask = jd.mask( frame )
        pose.get_pose( frame )
        cv2.imshow("Juggling", frame)
        cv2.imshow("Mask", pose.draw_landmarks_on_image( mask ) ) 

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()
        frame = orientation.correct_rotation(frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
