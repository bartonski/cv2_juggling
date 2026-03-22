import sys
import logging
import ffmpeg
import cv2
import pdb

class Dummy_logger:
    def __init__():
        pass

    def debug(message):
        pass

class Orientation:
    def __init__(self, file_path, configuration=None):
        self.rotation_code=None
        self.rotation = None
        self.file_path = file_path
        self.is_rotated = False
        self.logger = Dummy_logger
        if( configuration ):
            self.logger = configuration['logger']

        self.logger.debug( f"debugger working in orientation.py")

        try:
            # Probe the file to get metadata
            metadata = ffmpeg.probe(self.file_path)
            
            # Extract streams, looking for the first video stream
            streams = metadata.get('streams', [])
            
            for stream in streams:
                if stream.get('codec_type') == 'video':
                    # Check for side_data_list with rotation info
                    side_data_list = stream.get('side_data_list', [])
                    for side_data in side_data_list:
                        if 'rotation' in side_data:
                            self.logger.debug( f"side_data rotation: {side_data['rotation']}" )
                            self.rotation = int(side_data['rotation'])
                            self.rotation_code = self.get_rotation_code(self.rotation)
                            return None
                    
                    # Check if rotation is stored in tags
                    tags = stream.get('tags', {})
                    if 'rotate' in tags:
                        self.logger.debug( f"tags rotation: {tags['rotate']}" )
                        self.rotation = int(tags['rotate'])
                        self.rotation_code = self.get_rotation_code(self.rotation)
                        return None

        except ffmpeg.Error as e:
            print(f"Error processing the video file: {e}")
        if( self.rotation_code ):
            self.logger.debug( f"self.rotation_code: {self.rotation_code}")
        else:
            self.logger.debug( f"self.rotation_code: None")
            
        return None
            

    def get_rotation_code(self, rotation):
        """Rotation code is the correction needed to make the rotation 0."""
        
        if rotation == 90:
            return cv2.ROTATE_90_COUNTERCLOCKWISE
        elif (rotation == 180) or (rotation == -180):
            return cv2.ROTATE_180
        elif (rotation == 270) or (rotation == -90):
            return cv2.ROTATE_90_CLOCKWISE
        else:
            pass 

    def correct_rotation(self, frame):
        if self.rotation_code is not None:
            self.logger.debug( f"rotation corrected in correct_rotation()")
            return cv2.rotate(frame, self.rotation_code) 
        else:
            return frame

    def swap_width_and_height(self):
        rotation = self.rotation
        self.logger.debug( f"swap_width_and_heigh() rotation: {rotation}")
        if rotation:
            self.logger.debug( f"swap_width_and_heigh() rotation: {rotation}")
            if (rotation == 90 ) or (rotation == 270) or (rotation == -90):
                return True
        return False

# Example usage
# orientation = get_video_orientation('video.mp4')

def main():
    
    filename = str(sys.argv[-1])
    logger = logging.getLogger()
    logger.setlevel(logging.DEBUG)
    orientation = Orientation(filename, { 'logger': logger } )

    cap = cv2.VideoCapture(filename)
    cv2.namedWindow("Juggling")

    ret, frame = cap.read()
    # ret = True

    while ret:
        # Get layers
        frame = orientation.correct_rotation(frame)

        cv2.imshow(f"{filename}", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

