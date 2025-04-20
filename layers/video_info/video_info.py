import sys
import cv2

class VideoInfo:

    def __init__(self,config):
        self._cap=config['cap']
        self._filename=config['filename']
        self._width=config['width']
        self._height=config['height']
        self._frame_rate=config['frame_rate']
        self._frame_count=config['frame_count']
        #self._foo=config['foo']
        # ...

    def draw(self,image,arguments=None):

        cv2.putText(image, f"File Name: {self._filename}", (60, 120), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        cv2.putText(image, f"Width: {self._width}", (60, 180), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        cv2.putText(image, f"Height: {self._height}", (60, 240), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        cv2.putText(image, f"Frame rate: {self._frame_rate}", (60, 300), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        cv2.putText(image, f"Frame count: {self._frame_count}", (60, 360), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        cv2.putText(image, f"Image height: {image.shape[0]}", (60, 420), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        cv2.putText(image, f"Image width: {image.shape[1]}", (60, 480), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3 )
        # arguments is an optional dict
        # Draw on image 
        return image 

def main():

    filename = str(sys.argv[-1])
    cap = cv2.VideoCapture(filename)

    config = {
        'cap': cap
        , 'filename': filename
        , 'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        , 'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        , 'frame_rate': int(cap.get(cv2.CAP_PROP_FPS))
        , 'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # , 'foo': foo
        # , 'foo': foo
        # , 'foo': foo
    }
    video_info = VideoInfo( config )

    cv2.namedWindow("VideoInfo")

    ret, frame = cap.read()
    # ret = True

    while ret:
        # args contains data passed to draw
        cv2.imshow("VideoInfo", video_info.draw( frame ) )

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

