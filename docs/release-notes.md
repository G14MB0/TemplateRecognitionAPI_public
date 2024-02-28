
## Versions Schema:
a.b.c 
    - a: main version (0 = alpha, 1: beta, > 1 stable)
    - b: current version
    - c: curent revision


### 0.1.0
Template matching works. It uses templates and a frame (or a video) from a usb camera selected by index.
it returns the presence of the template/templates and their positions and confidences.

There is also the possibility to save the current frame with the matches (only if matches are present) in a local folder.

A first docs file has been created