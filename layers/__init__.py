class Layer:
    def __init__(self,config):
        self.config=config
        self.cv2=config["cv2"]
        self.image=config["image"]
