import cv2 

import numpy as np 

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, img = cap.read()
    
    #cv2.imshow("bruh",img)
    #print(img)
    
    cv2.imshow('Video',img)
    image = img
    image = img #cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Inverted',image)
    
    lower_red = np.array([0, 0, 0], dtype = "uint8") 
    upper_red= np.array([10, 10, 255], dtype = "uint8")
    
    #detects the lines of the board aswell, try to fix
    lower_blue = np.array([0, 0, 4], dtype = "uint8") 
    upper_blue= np.array([255, 50, 50], dtype = "uint8")
    
    #lower_black = np.array([190], dtype = "uint8") 
    #upper_black= np.array([255], dtype = "uint8")
    
    lower_black = np.array([70, 20, 85], dtype = "uint8") 
    upper_black= np.array([111, 93, 152], dtype = "uint8")
  
    mask_red = cv2.inRange(img, lower_red, upper_red)
    mask_blue = cv2.inRange(img, lower_blue, upper_blue)
    mask_black = cv2.inRange(image, lower_black, upper_black)
    
    red_out = cv2.bitwise_and(img, img, mask =  mask_red) 
    blue_out = cv2.bitwise_and(img, img, mask =  mask_blue) 
    green_out = cv2.bitwise_and(image, image, mask =  mask_black) 
    
    
    green_out = cv2.cvtColor(green_out, cv2.COLOR_BGR2GRAY)
    #green_out = 255-green_out
    
    ret, thresh = cv2.threshold(green_out,80,90,0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    imout = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    
    cv2.imshow("red color detection", red_out) 
    cv2.imshow("blue color detection", blue_out) 
    
    
    contours2 = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
    
    def centers(inner, outer):
        c = inner[..., 0].argsort()
        top_lef2, top_rit2 = sorted(inner[c][:2], key=list)
        bot_lef2, bot_rit2 = sorted(inner[c][-2:], key=list)
        c1 = outer[..., 0].argsort()
        c2 = outer[..., 1].argsort()
        top_lef, top_rit = sorted(outer[c1][:2], key=list)
        bot_lef, bot_rit = sorted(outer[c1][-2:], key=list)
        lef_top, lef_bot = sorted(outer[c2][:2], key=list)
        rit_top, rit_bot = sorted(outer[c2][-2:], key=list)
        yield inner.mean(0)
        yield np.mean([top_lef, top_rit, top_lef2, top_rit2], 0)
        yield np.mean([bot_lef, bot_rit, bot_lef2, bot_rit2], 0)
        yield np.mean([lef_top, lef_bot, top_lef2, bot_lef2], 0)
        yield np.mean([rit_top, rit_bot, top_rit2, bot_rit2], 0)
        yield np.mean([top_lef, lef_top], 0)
        yield np.mean([bot_lef, lef_bot], 0)
        yield np.mean([top_rit, rit_top], 0)
        yield np.mean([bot_rit, rit_bot], 0)
    
    def convex_hull(cnt):
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, peri * 0.02, True)
        return cv2.convexHull(approx).squeeze()
    
    
    #inner, outer = sorted(map(convex_hull, contours), key=len)
        
    #for x,y in cengers(inner,outer):
    #    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        
        
        #M = cv2.moments(i)
        #if m["m00"] !=0:
        #    cx = int(M['m10']/M['m00'])
        #    cy = int(M['m01']/M['m00'])
        #    cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
        #    cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
        #    
    #calibration z height - 39
    
    cv2.imshow("board color detection", img)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
       break
    
    
    