from .pose_detection import PoseDetector
from .contours import Contours

class Layer:
    def __init__(self,config):
        self.config=config

    # Create new image
    def image(self, image):
        self.image=config["image"]

    # Draw layer on top of image
    def draw(self, image):
        pass
from .grid_lines import GridLines