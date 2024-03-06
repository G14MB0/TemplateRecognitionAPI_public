'''
find coefficient also at 
https://www.calibdb.net/#
'''


import cv2
import numpy as np

# Carica i parametri della telecamera (ottenuti dalla calibrazione)
# camera_matrix = np.load("camera_matrix.npy")
# dist_coeffs = np.load("dist_coeffs.npy")

# Definisce una matrice della telecamera approssimativa
# Ad esempio, per una risoluzione 1080p, potresti avere qualcosa di simile:
camera_matrix = np.array([[1917.9816403671446, 0, 926.6434327683447], [0, 1911.0427128637868 , 559.8249210810895], [0, 0, 1]], dtype=np.float32)
# Usa un vettore di distorsione nullo se non conosci i coefficienti di distorsione
dist_coeffs = np.array([-0.03626273835527005,-0.7921296942309466,-0.0011375203379303846,0.0010923311887219979, 2.0635280952775354], dtype=np.float32)

# Inizializza il video
cap = cv2.VideoCapture(0)
cap.set(getattr(cv2, "CAP_PROP_FRAME_WIDTH"), 1920)
cap.set(getattr(cv2, "CAP_PROP_FRAME_HEIGHT"), 1080)
cap.set(getattr(cv2, "CAP_PROP_EXPOSURE"), -6.0)
cap.set(getattr(cv2, "CAP_PROP_BRIGHTNESS"), -50)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) 
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

parameters.minMarkerDistanceRate = 0.8
while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Rileva i markers
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        # Se almeno un marker è stato rilevato
        if ids is not None:

            # Calcola la posizione del marker rispetto alla camera
            rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.020, camera_matrix, dist_coeffs)
            print(tvecs[0][0][2])
            # 0.05 è la dimensione del marker in metri
            
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
