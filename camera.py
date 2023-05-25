import cv2 
from copy import deepcopy
import numpy as np 
import threading

class CameraMan():
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
        
     def startCam(self, verbose): #figure out how to do this
        cap = self.cap
        if not cap.isOpened():
            cap = cv2.VideoCapture(4)
        if verbose: print(cap.isOpened())
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        width = 640
        height = 480
        print(width)
        print(height)
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
    
    def cameraRunner(self,width,height,verbose):
        while True:
            cap = self.cap
            #print(cap.isOpened())
            ret, img = cap.read() 
            #cv2.imshow("bruh",img)
            #print(img)
            
            image = deepcopy(img)
            
            #Board color detection
            
            #setting color range 
            lower_pink = np.array([40, 20, 65], dtype = "uint8") 
            upper_pink= np.array([181, 111, 190], dtype = "uint8")     
            mask_pink = cv2.inRange(img, lower_pink, upper_pink) #colour mask
            blur = cv2.GaussianBlur(img, (5, 5),cv2.BORDER_DEFAULT) #gaussian blur version of image
            pink_out = cv2.bitwise_and(blur, blur, mask =  mask_pink) #creating the pink out mask
            pink_out = cv2.cvtColor(pink_out, cv2.COLOR_BGR2GRAY) #converting board mask to grayscale
            
            #centerpoint detection
            ret, thresh = cv2.threshold(pink_out,80,90,0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            imout = cv2.drawContours(image, contours, -1, (0,255,0), 3)
            
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
                        cv2.drawContours(image, [i], -1, (0, 255, 0), 2)
                        cv2.circle(image, (cx, cy), 7, (0, 0, 255), -1)
                        cv2.putText(image, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        
            if cx > 315 and cx  < 325 and cy > 235 and cy < 245:
                if verbose: print("centered")
            else:
                if verbose: print(cx-320,cy-240)
                
            self.offsetX = cx-320
            self.offsetY = cy-240
            #calibration z height - 70
            
            #crosshair
            cv2.line(image,(0,0),(int(width),int(height)),(255,0,0),5)
            cv2.line(image,(0,int(height)),(int(width),0),(255,0,0),5)
            
            
            
            
            #red block detection

            lower_red = np.array([0, 0, 0], dtype = "uint8") 
            upper_red= np.array([10, 10, 255], dtype = "uint8")
            mask_red = cv2.inRange(img, lower_red, upper_red)
            red_out = cv2.bitwise_and(img, img, mask =  mask_red) 
            
            red_bw = cv2.cvtColor(red_out, cv2.COLOR_BGR2GRAY)
            
            ret, thresh = cv2.threshold(red_bw,80,255,0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            imout = cv2.drawContours(image, contours, -1, (255,255,0), 3)
            
            contours2 = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            
            for i in contours2:
                M = cv2.moments(i)
                x,y,w,h = cv2.boundingRect(i)
                if w>10 and h>10:
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.drawContours(image, [i], -1, (255, 255, 0), 2)
                        cv2.circle(image, (cx, cy), 7, (255, 0, 0), -1)
                        cv2.putText(image, "red", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            #blue block detection
            
            lower_blue = np.array([0, 0, 4], dtype = "uint8") 
            upper_blue= np.array([255, 50, 10], dtype = "uint8")
            mask_blue = cv2.inRange(img, lower_blue, upper_blue)
            blue_out = cv2.bitwise_and(img, img, mask =  mask_blue) 
            
            blue_bw = cv2.cvtColor(blue_out, cv2.COLOR_BGR2GRAY)
            
            ret, thresh = cv2.threshold(red_bw,80,255,0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            imout = cv2.drawContours(image, contours, -1, (0,255,255), 3)
            
            contours2 = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            
            for i in contours2:
                M = cv2.moments(i)
                x,y,w,h = cv2.boundingRect(i)
                if w>10 and h>10:
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.drawContours(image, [i], -1, (0, 255, 255), 2)
                        cv2.circle(image, (cx, cy), 7, (255, 0, 0), -1)
                        cv2.putText(image, "blue", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            
            self.red_out = red_out #red blocks
            self.blue_out = blue_out #blue blocks
            self.pink_out = pink_out #board output
            self.image = image #marked output
            self.img = img #clean output