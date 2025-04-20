from .pose_detection import PoseDetector
from .contours import Contours
from .video_info import VideoInfo
from .grid_lines import GridLines

class Layer:
    def __init__(self,config):
        self.config=config

    # Create new image
    def image(self, image):
        self.image=config["image"]

    # Draw layer on top of image
    def draw(self, image):
        pass
