import cv2 

import numpy as np 

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, img = cap.read()
    
    #cv2.imshow("bruh",img)
    #print(img)
    
    cv2.imshow('Video',img)
    image = img
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Inverted',255-image)
    
    lower_red = np.array([0, 0, 0], dtype = "uint8") 
    upper_red= np.array([10, 10, 255], dtype = "uint8")
    
    #detects the lines of the board aswell, try to fix
    lower_blue = np.array([0, 0, 4], dtype = "uint8") 
    upper_blue= np.array([255, 50, 50], dtype = "uint8")
    
    lower_black = np.array([190], dtype = "uint8") 
    upper_black= np.array([255], dtype = "uint8")
  
    mask_red = cv2.inRange(img, lower_red, upper_red)
    mask_blue = cv2.inRange(img, lower_blue, upper_blue)
    mask_black = cv2.inRange(255-image, lower_black, upper_black)
    
    red_out = cv2.bitwise_and(img, img, mask =  mask_red) 
    blue_out = cv2.bitwise_and(img, img, mask =  mask_blue) 
    green_out = cv2.bitwise_and(image, image, mask =  mask_black) 
    
    cv2.imshow("red color detection", red_out) 
    cv2.imshow("blue color detection", blue_out) 
    cv2.imshow("board color detection", green_out) 
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
       break
    
    