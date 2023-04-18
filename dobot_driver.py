import pydobot
import time
import threading

class DobotBot:

    def __init__(self,port):
        self.dobot = pydobot.Dobot(port)
        self.start_x = 0
        self.start_y = 0
        self.start_z = 0
        self.red_stack = 5
        self.blue_stack = 5
        self.thread = None

    def move_bot(self,siit,sinna):
        if siit == 10:
            z = self.red_stack * 24 + self.start_z
            self.red_stack -= 1
        if siit == 11:
            z = self.blue_stack * 24 + self.start_z
            self.blue_stack -= 1
        else: z = 24 + self.start_z
        
        self.go_home()
        self.dobot.move_to(self.positions[siit][0], self.positions[siit][1], z, 0)
        self.dobot.suck(1)
        self.go_home()
        self.dobot.move_to(self.positions[sinna][0], self.positions[sinna][1], z, 0)
        self.dobot.suck(0)
        self.go_home()

    def move_increment(self,x,y,z):
        pose = self.dobot.pose() #tuple containing x,y,z,r,j1,j2,j3,j4
        self.dobot.move_to(pose[0]+x,pose[1]+y,pose[2]+z,0)
        time.sleep(1)
    
    def calibMove(self):
        print("movedcalib")
        x = self.x_offset
        y = self.y_offset
        self.move_increment(-x/10,-y/10,0)
        self.thread = None
        
    
    def calibrate(self, x_offset, y_offset):
        if self.thread is None:
            thread = threading.Thread(target=self.calibMove)
            thread.daemon = True
            self.thread = thread
            self.x_offset = x_offset
            self.y_offset = y_offset
            self.thread.start()
            print("started")
        
        
        #self.start_x = x
        #self.start_y = y
        #self.start_z = z

        #self.positions = (
        #            (x,y),
        #            (x,y+35),
        #            (x,y+70),
        #            (x+35,y),
        #            (x+35,y+35),
        #            (x+35,y+70),
        #            (x+70,y),
        #            (x+70,y+35),
        #            (x+70,y+70)
        #            )
    def setHome(self)
        self.start_x = self.dobot.pose()[0]
        self.start_y = self.dobot.pose()[1]
        self.start_z = self.dobot.pose()[2]
        
    def calibHeight(self):
        self.move_increment(0,0,70) #move to z height of 70 (from the ground)
        
    def go_home(self):
        self.dobot.move_to(self.start_x, self.start_y, self.start_z, 0)
    
    def succ(self, state):
        self.dobot.suck(state)
        
# 255 -35 -71


