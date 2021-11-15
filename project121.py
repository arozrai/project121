import cv2
import time
import numpy as np

# To save the output in a file - output.api
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output = cv2.VideoWriter("output.api",fourcc,20.0,(640,480))

frame = cv2.resize(frame,(640, 480))

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

#  Generating masks to detect color black
lower_black = np.array([104,153,70])
upper_black = np.array([30,30,0])

mask = cv2.inRange(hsv,lower_black,upper_black)

# Providing diluting effect to masks
mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN, np.ones((3, 3),np.uint8)) 
mask = cv2.morphologyEx(mask,cv2.MORPH_DILATE, np.ones((3, 3),np.uint8)) 

#Keeping only the part of the images without the red color 
#(or any other color you may choose) 
res = cv2.bitwise_and(img, img,mask=mask) 

#Generating the final output by merging res_1 and res_2 
final_output = cv2.addWeighted(res, 1,0) 
output_file.write(final_output) 

#Displaying the output to the user 
cv2.imshow("magic", final_output) 
cv2.waitKey(1)

cap.release() 
out.release() 
cv2.destroyAllWindows() 