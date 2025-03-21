import cv2
import sys
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np


class PoseDetector:

    def __init__(self,config):
        self.model_asset_path=config['model_asset_path']
        base_options = python.BaseOptions(model_asset_path=self.model_asset_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def draw_landmarks_on_image(self,image):
        cv_mat = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_mat)
        rgb_image = mp_image.numpy_view()
        detection_result = self.detection_result
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(
                x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
        return cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

    def get_pose(self,frame):
        self.cv_mat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.cv_mat)

        self.detection_result = self.detector.detect(image)

    def image(self):
        return self.pose_image

    def detection_result(self):
        return self.detection_result

def main():
    config = {
        'model_asset_path': 'pose_landmarker_heavy.task'
    }
    filename = str(sys.argv[-1])

    cap = cv2.VideoCapture(filename)

    pose = PoseDetector( config )

    cv2.namedWindow("Pose")

    ret, frame = cap.read()
    # ret = True

    while ret:
        # Get layers
        pose.get_pose( frame )
        cv2.imshow("Pose", pose.draw_landmarks_on_image( frame ) )

        key = cv2.waitKey(1)
        if key == 27:
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

