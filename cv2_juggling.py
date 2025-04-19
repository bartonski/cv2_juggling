import cv2
import sys
from core.detector import Detector
from filters import Orientation
from layers import PoseDetector
from layers import Contours

def main():
    filename = str(sys.argv[-1])
    config = {
        'detector':{
            'detector_history': 100,
            'detector_threshold': 40,
            'area_threshold': 50,
            'grey_threshold': 255
        }
        , 'pose_detector':{
            'model_asset_path': 'layers/pose_detection/pose_landmarker_heavy.task'
        }
        , 'contours':{
            'outline_color': (0,255,0)
            , 'outline_thickness': 2
        }
    }
    # should populate orientation_config, pass to Orientation

    cap = cv2.VideoCapture(filename)
    orientation = Orientation(filename)
    jd = Detector(config.get('detector')) 
    pose = PoseDetector( config.get('pose_detector'))
    cntrs = Contours( config.get('contours'))

    cv2.namedWindow("Juggling")
    cv2.namedWindow("Mask")

    ret, frame = cap.read()
    frame = orientation.correct_rotation(frame)
    
    # ret = True

    while ret:
        mask = jd.mask( frame )
        pose.get_pose( frame )
        frame = cntrs.draw( frame, { 'contours':jd.contours(mask) } )
        cv2.imshow("Juggling", frame)
        cv2.imshow("Mask", pose.draw( mask ) ) 

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()
        frame = orientation.correct_rotation(frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
