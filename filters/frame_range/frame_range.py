import sys
import cv2

class FrameRange:

    def __init__(self,config):
        self._start_frame=config['start_frame']
        self._cap=config['cap']
        self._frame_count=int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if( config.get('end_frame') and config['end_frame'] < self._frame_count):
            self._end_frame=config['end_frame']
        else:
            self._end_frame=self._frame_count
        self._current_frame=0
        # ...

    def check_frame_range(self,ret):
        # ret is the return value of cv2.VideoCapture.read()
        # arguments is an optional dict
        # Draw on image 
        next_frame = False
        end = False
        if(ret):
            self._current_frame += 1
            if( self._current_frame < self._start_frame):
                next_frame = True
            if( self._current_frame > self._end_frame):
                end = True
        return end, next_frame

    def current_frame(self):
        return self._current_frame

    def draw(self, frame, args=None):
        cv2.putText(frame, f"Frame number {self._current_frame}", (60, 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        return frame

def main():
    filename = str(sys.argv[-1])
    cap = cv2.VideoCapture(filename)
    user_frame_delay = 100
    running = 0
    frame_delay = running * user_frame_delay
    toggle = [1, 0]

    config = {
        'cap' : cap
        , 'start_frame': 11
        , 'end_frame': 660
        , 'print_frame_number': True
    }

    framerange = FrameRange( config )

    cv2.namedWindow("Frame Range", cv2.WINDOW_FULLSCREEN)

    ret, frame = cap.read()
    # ret = True

    while ret:
        end, next_frame = framerange.check_frame_range(ret) 
        if (next_frame):
            ret, frame = cap.read()
            continue
        if (end):
            break
        cv2.imshow("Frame Range", framerange.draw(frame) )


        key = cv2.waitKey(frame_delay)
        if key == 27:
            break
        elif key == ord(' '):
            running = toggle[running]
            frame_delay = running * user_frame_delay
        elif key == ord('f'):
            frame_delay = 0
        elif key == ord('>'):
            user_frame_delay += 1
            frame_delay = running * user_frame_delay
        elif key == ord('<'):
            user_frame_delay -= 1
            frame_delay = running * user_frame_delay
        ret, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

