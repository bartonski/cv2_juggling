## TODO

* Add argument handling
* Import configuration file
* Use numpy.ndarray.shape (i.e. image.shape) to determine width and height
* Document code
* Test code
* Cropping
    * ~~Write Crop class~~
    * Call Crop from `cv2_juggling.py`
* Create VideoCaptureContext class
    * It should accept filter classes and yield filtered frames
    * See notes in [ChatGPT](https://chatgpt.com/canvas/shared/680d34873e98819189fa81d941d8282b)
* Write 'World' or 'Data' class that holds data from filter and core classes that may be used by output filters.  I'd like to do things like
    * Coloring contours by size threshold
    * Coloring contours or centers by type (hand, prop)
* Trails can be created by drawing centers on a transparent overlay. See code [here](https://chatgpt.com/canvas/shared/680d2f48c7d881919cdcd12855e650c9)

## Notes

