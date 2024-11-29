This is my second attempt to create a computer vision based juggling tracker.

Because my first attempt became too complicated, I'm trying to build this one from very basic pieces, which retain as much of their simplicity as possible.

Here's what this consists of:

* `video_read.py`: Takes a video file as a command line option, read it frame by frame, display video in window. Essentially just a lame video player. Press <kbd>Esc</kbd> to quit.

* `cv2_juggling.py`: The idea here is that video will be read frame at a time,
and fed into a function that processes the video. Processing happens through a
number of passes, each pass can output image data and/or text. Video data can be output as image files written to disk or layered on output video. Output video can be displyed on screen and/or written to a video file. Here are the passes and their output:
    * Background Subtraction

      | Name | Description                                                      | Type  |
      |------|------------------------------------------------------------------|-------|
      | Mask | Black and white image with foreground [moving objects] in white  | Image |
      | Contours | Outline of masks                                             | Image |
      | Centers | Points at the centers of Contours                       | Image, Text |
      | Trails  | History of centers.                                           | Image |
      | Color Range | Show mask based on color range                            | Image |
      | ROI         | Show Region of interest                                   | Image |

    * Tracking: Compare center of current list of contours. If center is within tracking radius, it's condisered to be the same object. 

      | Name | Description                                                      | Type  |
      |------|------------------------------------------------------------------|-------|
      | Tracking Area | Show area within tracking radius                        | Image |
      | Sparks   | Line between line previous center and current                | Image |
      | Prediction | Show kalman filter prediction                        | Image, Text |
      | Kalman Difference | Show difference between center and Kalman prediction | Image|

    * Pose estimation

      | Name | Description                                                      | Type  |
      |------|------------------------------------------------------------------|-------|
      | Hands    | Show hands based on mediapipe                                | Image |
      | Pose     | Show pose based on mediapipe                                 | Image |

    * Display

      | Name | Description                                                      | Type  |
      |------|------------------------------------------------------------------|-------|
      | Grid     | Show grid                                                    | Image |
      | BPM      | beats (throws) per minute                                    | Image |
      | Dwell Ratio   | Show dwell time as a ratio to BPM.                      | Image |
      | Object Labels | Show what type of object is being displayed             | Image |
      | Frame Number  | Show frame number                                       | Image |
      | Average throw | Show path of average throw                              | Image |
      | Site Swap throw | Show path of Even/Odd/Both site swaps                 | Image |
      | Catch count   | Show the current number of catches                | Image, Text |

## Resources

### Videos

* [Object Tracking with Opencv and Python - YouTube](https://www.youtube.com/watch?v=O3b8lVF93jU)
* [Predict trajectory of an Object with Kalman filter - YouTube](https://www.youtube.com/watch?v=3iqRhbXBVRE)
* [Identify any object with python - Beginner Guide - YouTube](https://www.youtube.com/watch?v=hVRz29N_zpg) -- intro to YOLO.

### Web pages

* [OpenCV - Stream video to web browser/HTML page - PyImageSearch](https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/)

