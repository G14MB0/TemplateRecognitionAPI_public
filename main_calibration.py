import numpy as np
import cv2 as cv
import glob
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 25, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*10,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:10].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('calibrationImages/*.jpg')

cap = cv.VideoCapture(0)  # 0 is usually the default webcam
cap.set(getattr(cv, "CAP_PROP_FRAME_WIDTH"), 1920)
cap.set(getattr(cv, "CAP_PROP_FRAME_HEIGHT"), 1080)

while True:
    ret, frame = cap.read()
    # ret, frame = (True, cv2.imread("./image.jpg"))
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        raise RuntimeError("Can't receive frame (stream end?). Exiting ...")
    
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(frame, (5,5), None)

    if ret == True:
        print("trovata")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(frame, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(frame, (7,10), corners2, ret)
        cv.imshow('img', frame)
    else:
        cv.imshow('img', frame)
        
    # Break the loop on pressing 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break

# for fname in images:
#     img = cv.imread(fname)
#     gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     # Find the chess board corners
#     ret, corners = cv.findChessboardCorners(gray, (7,10), None)
#     # If found, add object points, image points (after refining them)
#     if ret == True:
#         print("trovata")
#         objpoints.append(objp)
#         corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
#         imgpoints.append(corners2)
#         # Draw and display the corners
#         cv.drawChessboardCorners(img, (7,10), corners2, ret)
#         cv.imshow('img', img)
#         cv.waitKey(500)
# cv.destroyAllWindows()

# ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# print(ret, mtx, dist, rvecs, tvecs)