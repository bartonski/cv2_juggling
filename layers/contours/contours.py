import cv2

class Contours:

    def __init__(self,config):
        self._outline_color=config['outline_color']
        self._outline_thickness=config['outline_thickness']

    def draw(self,image,arguments=None):
        cv2.drawContours(
            image                       # image to draw on
            , arguments.get('contours') # list of contours to draw
            , -1                        # index of contour to draw (-1 -> all contours)
            , self._outline_color       # color of outline
            , self._outline_thickness   # thickness
        )
        return image 

def main():
    config = {
        'detector':{
            'detector_history': 100,
            'detector_threshold': 40,
            'area_threshold': 50,
            'grey_threshold': 255
        }
        , 'contours':{
            'outline_color': (0,255,0)
            , 'outline_thickness': 2
        }
    }
    filename = str(sys.argv[-1])

    cap = cv2.VideoCapture(filename)

    jd = Detector( config.get('detector') )
    cntrs = Contours( config.get('contours') )

    cv2.namedWindow("Contours")

    ret, frame = cap.read()
    # ret = True

    while ret:
        # args contains data passed to draw
        mask = jd.mask( frame )
        args = { contours:jd.contours(mask) }
        cv2.imshow("Contours", contours.draw( frame, args ) )

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    from filters import Orientation
    from core.detector import Detector

    main()


# cv2.drawContours(
#     image               # image to draw on
#     , contours          # list of contours to draw
#     , -1                # index of contour to draw (-1 -> all contours)
#     , (0, 255, 0)       # color of outline
#     , 2                 # thickness
# )
