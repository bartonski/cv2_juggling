import sys
import cv2

class GridLines:

    def __init__(self,config):
        self._height = config['height']
        self._width = config['width']
        self._x_offset = config['x_offset']
        self._y_offset = config['y_offset']
        self._grid_color = config['grid_color']
        self._grid_linewidth = config['grid_linewidth']
        self._grid_spacing = config['grid_spacing']
        # ...

    def draw(self,image,arguments=None):
        # Draw horizontal lines
        for y in range(self._y_offset, self._height, self._grid_spacing):
            cv2.line(image, (0,y), (self._width,y), self._grid_color, self._grid_linewidth)

        # Draw vertical lines
        for x in range(self._x_offset, self._width, self._grid_spacing):
            cv2.line(image, ( x, 0), (x, self._height), self._grid_color, self._grid_linewidth  )
        # arguments is an optional dict
        # Draw on image 
        return image 

def main():

    filename = str(sys.argv[-1])
    cap = cv2.VideoCapture(filename)

    config = {
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        , 'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        , 'x_offset': 0
        , 'y_offset': 0
        , 'grid_color': ( 0x7F, 0x7F, 0x7F )
        , 'grid_linewidth': 4
        , 'grid_spacing': 100
    }
    grid_lines = GridLines( config )

    cv2.namedWindow("GridLines")

    ret, frame = cap.read()

    while ret:
        cv2.imshow("GridLines", grid_lines.draw( frame ) )

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

