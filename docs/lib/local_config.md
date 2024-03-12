
::: lib.local_config


---
# All Local Settings

All this local settings are in a .txt file in the folder %USERPROFILE%\TemplateRecognitionAPI.
They are **case sensitive** and if changed directly from that file, there must no be spaces between name, = and value (for example: name=value and not name = value)

- template_folder: the folder from where to search for all template to use in template matching
- saving_folder: the folder where to save the matched templates
- MATCHING_THRESHOLD: a global value for template matching. tm return positive matching if confidence is over this value
- is_colored: If use colored template and frame during template matching
- LIVE_TRIGGER_INTERVAL: The live trigger is "as fast as possible" but the websocket follow this interval (at each cycle, it sleeps for this, in seconds)
- DEFAULT_DISTANCE: Default setup (camera) distance from the target. if no specified in the template_setting.json, this will be used (in centimeters)
- DEFAULT_RESOLUTION: (width, height)
- CAMERA_MATRIX: Camera Matrix Calibration coefficient, for example [[1917.9816403671446, 0, 926.6434327683447],[0, 1911.0427128637868 , 559.8249210810895],[0, 0, 1]]. Find in technical specifications or at https://www.calibdb.net/#
- CAMERA_COEFFICIENTS: Camera distorsion coefficient. Find in technical specifications or at https://www.calibdb.net/#
- ARUCO_SIZE: aruco tag dimensions in meters (in meters)