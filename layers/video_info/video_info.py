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
        self._shadow_offset=config['shadow_offset']
        self._font_color=config['font_color']
        self._shadow_color=config['shadow_color']
        self._font_scale=config['font_scale']
        self._font=config['font']
        self._thickness=config['thickness']
        #self._foo=config['foo']
        # ...

    def _draw_text(self,image,text,location,font,font_scale,font_color,thickness):
        shadow_location = (location[0]+self._shadow_offset[0],
                           location[1]+self._shadow_offset[1] )
        shadow_color = self._shadow_color
        
        cv2.putText(image,text,shadow_location,font,font_scale,shadow_color,thickness)
        cv2.putText(image,text,location,font,font_scale,font_color,thickness)

    def draw(self,image,arguments=None):
        font = self._font
        scale = self._font_scale
        font_color = self._font_color
        thickness = self._thickness

        s=image.shape
        header_height = image.shape[1] / 5

        info_lines = [
              f"File Name: {self._filename}"
            , f"Width: {self._width}"
            , f"Height: {self._height}"
            , f"Frame rate: {self._frame_rate}"
            , f"Frame count: {self._frame_count}"
            , f"Image width: {s[0]}"
            , f"Image height: {s[1]}"
            , f"Line height: "
            , f"Font scale: "
        ]

        count = len(info_lines) + 1
        (box_width, box_height), baseline = cv2.getTextSize( info_lines[0], font, 1, thickness )

        line_height=int(header_height/count)
        font_scale = scale * baseline * (count)/(count+8)

        info_lines[-2] = f"Line height: {line_height}"
        info_lines[-1] = f"Font scale: {font_scale}"
        
        x = 60
        y = line_height
        for line in info_lines:
            y = y + line_height
            self._draw_text(image,line, (x,y), font, font_scale, font_color, thickness)
        
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
        , 'shadow_offset': (2, 2)
        , 'font_color': (255,255,255)
        , 'shadow_color': (0,0,0)
        , 'font_scale': 1
        , 'font': cv2.FONT_HERSHEY_PLAIN
        , 'thickness': 3
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

