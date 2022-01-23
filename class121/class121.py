import cv2
import time
import numpy as np

# To save the output in a file - output.api
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output = cv2.VideoWriter("output.api",fourcc,20.0,(640,480))

# starting camera
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# allowing the camera to start by making the code sleep for 2 secs
time.sleep(2)
bg = 0

# capturing background for 60 seconds
for i in range(60):
    ret, bg = cap.read()

# Flipping background
bg = np.flip(bg, axis=1)

# Reading captured frame until camera opens
while (cap.isOpened()): 
    ret, img = cap.read() 
    if not ret: 
        break 
    #Flipping the image for consistency 
    img = np.flip(img, axis=1)

    #  Coverting the color to BGR to HSV
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #  Generating masks to detect color red
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])

    mask_1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])

    mask_2 = cv2.inRange(hsv,lower_red,upper_red)

    mask_1 = mask_1+mask_2

    # Providing diluting effect to masks
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_OPEN, np.ones((3, 3),np.uint8)) 
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_DILATE, np.ones((3, 3),np.uint8)) 

    #Selecting only the part that does not have mask one and saving in mask2 
    mask_2 = cv2.bitwise_not(mask_1) 

    #Keeping only the part of the images without the red color 
    #(or any other color you may choose) 
    res_1 = cv2.bitwise_and(img, img,mask=mask_2) 

    #Keeping only the part of the images with the red color 
    #(or any other color you may choose) 
    res_2 = cv2.bitwise_and(bg, bg,mask=mask_1)

    #Generating the final output by merging res_1 and res_2 
    final_output = cv2.addWeighted(res_1, 1, res_2, 1,0) 
    output_file.write(final_output) 

    #Displaying the output to the user 
    cv2.imshow("magic", final_output) 
    cv2.waitKey(1)

cap.release() 
out.release() 
cv2.destroyAllWindows() 