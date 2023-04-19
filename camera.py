import cv2 
from copy import deepcopy
import numpy as np 
import threading

class cameraMan():
    def __init__(self):
        self.cap = cv2.VideoCapture(4)
        if self.cap.isOpened():
            print("Open")
        else:
            print("Failed to open camera")
        self.offsetX = 0
        self.offsetY = 0
        self.task = None
        
        self.red_out = None
        self.blue_out = None
        self.pink_out = None
        self.image = None
        self.img = None
        
    def cameraRunner(self,width,height,verbose):
        while True:
            cap = self.cap
            #print(cap.isOpened())
            ret, img = cap.read() 
            #cv2.imshow("bruh",img)
            #print(img)
            
            image = deepcopy(img)
            
            lower_red = np.array([0, 0, 0], dtype = "uint8") 
            upper_red= np.array([10, 10, 255], dtype = "uint8")
            
            #detects the lines of the board aswell, try to fix
            lower_blue = np.array([0, 0, 4], dtype = "uint8") 
            upper_blue= np.array([255, 50, 10], dtype = "uint8")
            
            #lower_black = np.array([190], dtype = "uint8") 
            #upper_black= np.array([255], dtype = "uint8")
            
            lower_pink = np.array([40, 20, 65], dtype = "uint8") 
            upper_pink= np.array([181, 111, 190], dtype = "uint8")     
          
            mask_red = cv2.inRange(img, lower_red, upper_red)
            mask_blue = cv2.inRange(img, lower_blue, upper_blue)
            mask_pink = cv2.inRange(img, lower_pink, upper_pink)
            
            blur = cv2.GaussianBlur(img, (5, 5),cv2.BORDER_DEFAULT)
            
            red_out = cv2.bitwise_and(img, img, mask =  mask_red) 
            blue_out = cv2.bitwise_and(img, img, mask =  mask_blue) 
            pink_out = cv2.bitwise_and(blur, blur, mask =  mask_pink) 
            
                
            pink_out = cv2.cvtColor(pink_out, cv2.COLOR_BGR2GRAY)
            #green_out = 255-green_out
    
            
            ret, thresh = cv2.threshold(pink_out,80,90,0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            imout = cv2.drawContours(img, contours, -1, (0,255,0), 3)
            
            
            contours2 = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            
            cx = 0
            cy = 0
            
            for i in contours2:
                M = cv2.moments(i)
                x,y,w,h = cv2.boundingRect(i)
                if w>20 and h>20 and x>100 and x<540:
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
                        cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                        cv2.putText(img, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        
            if cx > 315 and cx  < 325 and cy > 235 and cy < 245:
                if verbose: print("centered")
            else:
                if verbose: print(cx-320,cy-240)
                
            self.offsetX = cx-320
            self.offsetY = cy-240
            #calibration z height - 70
            
            cv2.line(img,(0,0),(int(width),int(height)),(255,0,0),5)
            cv2.line(img,(0,int(height)),(int(width),0),(255,0,0),5)
            #cv2.imshow("board color detection", img)
            #cv2.imshow('Video',image)
            #cv2.imshow("red color detection", red_out) 
            #cv2.imshow("blue color detection", blue_out) 
            #cv2.imshow('colorrr',green_out)
            
            self.red_out = red_out
            self.blue_out = blue_out
            self.pink_out = pink_out
            self.image = image
            self.img = img
    
        
    def startCam(self, verbose): #figure out how to do this
        cap = self.cap
        if not cap.isOpened():
            cap = cv2.VideoCapture(4)
        if verbose: print(cap.isOpened())
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if verbose: print(width,height) 
        thread = threading.Thread(target=self.cameraRunner, args=(width,height,verbose))
        thread.daemon = True
        thread.start()
        self.thread = thread
   
    def getCam(self,camera):
        output = eval("self."+camera)
        return (output)
    
    def stopCam(self):
        print("stopping")
        self.cap.release()
        self.thread.stop()
        print("stopped")
        return True
        
    def getOffset(self):
        return self.offsetX,self.offsetY
        
    
    
    
        