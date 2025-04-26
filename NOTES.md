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
    * See notes in [ChatGPT](https://chatgpt.com/g/g-cKXjWStaE-python/c/6754bad6-1810-800f-8e55-cf88ce77057e) under **Command List Summary**
* Write 'World' or 'Data' class that holds data from filter and core classes that may be used by output filters.  I'd like to do things like
    * Coloring contours by size threshold
    * Coloring contours or centers by type (hand, prop)

## Notes
