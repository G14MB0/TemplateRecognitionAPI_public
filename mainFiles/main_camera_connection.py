import cv2

# This is the RTSP URL for the camera, replace with your actual URL
rtsp_url = 'rtsp://root:hil@192.168.100.100/axis-media/media.amp'

# Use OpenCV to capture the video stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream was opened successfully
if not cap.isOpened():
    print('Error opening video stream')
else:
    try:
        # Read the stream in a loop
        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if ret:
                # Display the resulting frame
                cv2.imshow('Frame', frame)

                # Press Q on keyboard to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    except KeyboardInterrupt:
        print('Stream interrupted.')

    finally:
        # When everything done, release the video capture object
        cap.release()
        cv2.destroyAllWindows()

print('Stream ended.')
