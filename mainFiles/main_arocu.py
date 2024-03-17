# '''
# find coefficient also at 
# https://www.calibdb.net/#
# '''


import cv2
import numpy as np

# # Carica i parametri della telecamera (ottenuti dalla calibrazione)
# # camera_matrix = np.load("camera_matrix.npy")
# # dist_coeffs = np.load("dist_coeffs.npy")

# # Definisce una matrice della telecamera approssimativa
# # Ad esempio, per una risoluzione 1080p, potresti avere qualcosa di simile:
# camera_matrix = np.array([[773.2477068318896,0,619.8203782284338],[0,781.6348832411827,386.3898940018346],[0,0,1]], dtype=np.float32)
# # Usa un vettore di distorsione nullo se non conosci i coefficienti di distorsione
# dist_coeffs = np.array([-0.0964677935098207,0.1455956101827609,0.004942509954771297,-0.0021712277799483715,-0.09228500543931754], dtype=np.float32)

# # Inizializza il video
# cap = cv2.VideoCapture(0)
# cap.set(getattr(cv2, "CAP_PROP_FRAME_WIDTH"), 1280)
# cap.set(getattr(cv2, "CAP_PROP_FRAME_HEIGHT"), 720)
# cap.set(getattr(cv2, "CAP_PROP_EXPOSURE"), -6.0)
# cap.set(getattr(cv2, "CAP_PROP_BRIGHTNESS"), -50)

# dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) 
# parameters =  cv2.aruco.DetectorParameters()
# detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# parameters.minMarkerDistanceRate = 0.02
# while True:
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         # Rileva i markers
#         corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

#         # Se almeno un marker è stato rilevato
#         if ids is not None:

#             # Calcola la posizione del marker rispetto alla camera
#             rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.020, camera_matrix, dist_coeffs)
#             print(tvecs[0][0][2])
#             # 0.05 è la dimensione del marker in metri
            
#             # Visualizza i marker e la loro orientazione
#             for rvec, tvec in zip(rvecs, tvecs):
#                 cv2.aruco.drawDetectedMarkers(frame, corners, ids)
#                 cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.1)
        
#         cv2.imshow('Frame', frame)
        
#         # Premi 'q' per uscire dal loop
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# cap.release()
# cv2.destroyAllWindows()


from lib.template_recognition.methods.aruco_operations import calculateSetupDistance
print(calculateSetupDistance((1280, 720), 0))