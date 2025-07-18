import cv2
import sys
from core.detector import Detector
from filters import Orientation
from filters import FrameRange
from layers import PoseDetector
from layers import Contours
from layers import GridLines
from layers import VideoInfo

def main():
    filename = str(sys.argv[-1])
    cap = cv2.VideoCapture(filename)
    filter_config = {
        'frame_range':{
            'cap': cap,
            'start_frame': 11,
            'end_frame': 660,
            'print_frame_number': True
        }
    }

    core_config = {
        'detector':{
            'detector_history': 100,
            'detector_threshold': 90,
            'area_threshold': 50,
            'grey_threshold': 255
        }
        , 'contours':{
            'outline_color': (0,255,0)
            , 'outline_thickness': 2
        }
    }

    layer_config = {
        'video_info':{
            'cap': cap
            , 'filename': filename
            , 'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            , 'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            , 'frame_rate': int(cap.get(cv2.CAP_PROP_FPS))
            , 'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            , 'shadow_offset': (2, 2)
            , 'font_color': (255,255,255)
            , 'shadow_color': (0,0,0)
            , 'font_scale': 0.5
            , 'font': cv2.FONT_HERSHEY_PLAIN
            , 'thickness': 2
        }
        , 'pose_detector':{
            'model_asset_path': 'layers/pose_detection/pose_landmarker_heavy.task'
        }
    }
    # should populate orientation_config, pass to Orientation

    orientation = Orientation(filename)
    framerange = FrameRange( filter_config.get('frame_range'))
    jd = Detector(core_config.get('detector')) 
    pose = PoseDetector( layer_config.get('pose_detector'))
    cntrs = Contours( core_config.get('contours'))
    video_info = VideoInfo( layer_config.get('video_info'))

    height =  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    if( orientation.swap_width_and_height ):
        height, width = width, height
        
    grid_lines= {
        'height': height
        , 'width': width
        , 'x_offset': 0
        , 'y_offset': 0
        , 'grid_color': ( 0x7F, 0x7F, 0x7F )
        , 'grid_linewidth': 4
        , 'grid_spacing': 100
    }

    grid_lines = GridLines( grid_lines )

    cv2.namedWindow("Juggling")
    cv2.namedWindow("Mask")

    ret, frame = cap.read()
    frame = orientation.correct_rotation(frame)
    
    # ret = True

    while ret:
        end, next_frame = framerange.check_frame_range(ret)
        if (next_frame):
            ret, frame = cap.read()
            continue
        if (end):
            break

        mask = jd.mask( frame )
        pose.get_pose( frame )
        frame = grid_lines.draw(frame)
        frame = video_info.draw(frame)
        frame = framerange.draw(frame)
        frame = cntrs.draw( frame, { 'contours':jd.contours(mask) } )
        frame = pose.draw(frame)
        cv2.imshow("Juggling", frame)
        # cv2.imshow("Mask", pose.draw( mask ) ) 

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()
        frame = orientation.correct_rotation(frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
