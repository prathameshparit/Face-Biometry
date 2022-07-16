# program to capture single image from webcam in python

# importing OpenCV library
import cv2
import os
# initialize the camera
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that
cam_port = 0
cam = cv2.VideoCapture(cam_port)

# reading the input using the camera
result, image = cam.read()

# If image will detected without any error, 
# show result
if result:
    name = input("Enter the name: ")
    # showing result, it take frame name and image 
    # output
    cv2.imshow(name, image)

    # saving image in local storage
    path = 'log'
    cv2.imwrite(os.path.join(path, name+'.jpg'), image)

    # If keyboard interrupt occurs, destroy image 
    # window
    cv2.waitKey(0)
    cv2.destroyWindow(name)

# If captured image is corrupted, moving to else part
else:
    print("No image detected. Please! try again")