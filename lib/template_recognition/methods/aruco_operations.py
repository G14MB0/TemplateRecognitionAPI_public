import cv2
import numpy as np
from lib import local_config
from typing import Tuple, List, Dict
from lib.global_var import logger



def calculateSetupDistance(cameraRes: Tuple[int, int], cameraIndex: int) -> float:
    """This method calculate the distance from the camera and a set of ARUCO tag, taken from the first 50 in order of ids.
    The calculation is made by considering the mean distance along z axis (the camera pointing direction) of all the aruco detected.
    - It's very important to insert the camera matrix and distorsion coefficient for the used camera in local_setting, otherwise the calculation
    will be wrong!!

    Args:
        cameraRes (Tuple[int, int]): camera resolution (x,y)
        cameraIndex (int): index of the camera

    Returns:
        float: the mean distance in cm
    """    
    print("Start setup distance Calculation...")
    camera_matrix = np.array(eval(local_config.readLocalConfig().get("CAMERA_MATRIX", "None")), dtype=np.float32)
    dist_coeffs = np.array(eval(local_config.readLocalConfig().get("CAMERA_COEFFICIENTS", "None")), dtype=np.float32)

    if camera_matrix is None or dist_coeffs is None:
        raise RuntimeError("No camera matrix or camera coefficient in local_config. please add it!")

    print(f"Initializing camera with index {cameraIndex}")

    # Initialize the video capture
    cap = cv2.VideoCapture(cameraIndex, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cameraRes[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cameraRes[1])
    cap.set(cv2.CAP_PROP_EXPOSURE, -6.0)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, -50)

    print("Start ARUCO detection")

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) 
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # Adjust the minimum marker distance rate
    parameters.minMarkerDistanceRate = 0.02

    # Dictionary to store Z-distances for each marker ID
    z_distances: Dict[int, List[float]] = {}

    for _ in range(30):
        ret, frame = cap.read()
        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

            if ids is not None:
                rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, float(local_config.readLocalConfig().get("ARUCO_SIZE", "0.020")), camera_matrix, dist_coeffs)
                
                for i, id in enumerate(ids.flatten()):
                    z_distance = tvecs[i][0][2]
                    if id in z_distances:
                        z_distances[id].append(z_distance)
                    else:
                        z_distances[id] = [z_distance]
                
                # Visualizza i marker e la loro orientazione
                for rvec, tvec in zip(rvecs, tvecs):
                    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                    cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.1)
                    

            cv2.imshow('Frame', frame)
            # Premi 'q' per uscire dal loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    cap.release()
    cv2.destroyAllWindows()

    # Assuming valid_markers is a dictionary with marker IDs as keys and lists of distances as values
    valid_markers = {id: distances for id, distances in z_distances.items() if len(distances) >= 15}

    # Calculate the mode of Z-distances for each marker
    means = []
    for distances in valid_markers.values():
        if distances:  # Check if the list of distances is not empty
            mean_result = sum(distances)/len(distances)
            print(mean_result)
            means.append(mean_result)

    # Calculate the average of the modes if there are any valid markers
    if means:
        average_mean = np.mean(means)
        print(f"distance detected: {average_mean * 100}")
        return average_mean * 100
    else:
        logger.warning("No valid markers detected in more than 50% of the frames.")
        return -1

