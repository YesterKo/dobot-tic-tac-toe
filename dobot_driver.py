import pydobot
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

    def move_to(self,x,y,z,r):
        self.dobot.move_to(x,y,z,r)
        prevpos=[0,0,0]
        #this needs to be done because the wait=True in dobot.move_to is broken and stops the bot, so I made my own
        while True: #I can't believe this works lmao
            pose = self.dobot.pose()
            if [pose[0],pose[1],pose[2]]==prevpos:
                return;
            prevpos = [pose[0],pose[1],pose[2]]
                
    def move_increment(self,x,y,z):
        pose = self.dobot.pose() #tuple containing x,y,z,r,j1,j2,j3,j4
        self.move_to(pose[0]+x,pose[1]+y,pose[2]+z,0)
        
    def go_home(self):
        self.move_to(self.start_x, self.start_y, self.start_z, 0)
    
    def succ(self, state):
        self.dobot.suck(state)

    def place_block(self,color,pos): #pos 0-8, color blue or red
        #pos 3
        if color == "r":
            size = self.red_stack
            stack = 9
        else:
            size = self.blue_stack
            stack = 10
        
        height = self.start_z-64+24*size
        print(height)
        pose = self.dobot.pose()
        positions = self.positions
        
        try:
            self.move_to(pose[0],pose[1],height,0)
            self.move_to(positions[stack][0],positions[stack][1],height,0)
            self.move_increment(0,0,-10)
            self.succ(True)
            self.move_increment(0,0,30)
            self.move_to(positions[pos][0],positions[pos][1],height+30,0)
            self.move_to(positions[pos][0],positions[pos][1],self.start_z-56,0)
            self.succ(False)
            self.move_increment(0,0,30)
            self.go_home()
        except:
            print("Something broke, attempting to return home...")
            try:
                self.succ(False)
                pose = self.dobot.pose()
                self.move_to(pose[0],pose[1],100,0)
                self.go_home()
            except:
                print("Error returning home")
        
        size-=1
        
        if color == "r":
            self.red_stack=size
        else:
            self.blue_stack=size
    
    def remove_block(self,color,pos): #move block back to it's stack
        if color == "r":
            size = self.red_stack
            stack = 9
        else:
            size = self.blue_stack
            stack = 10
            
        height = self.start_z-40+24*size 
        positions = self.positions
        
        self.move_to(positions[pos][0],positions[pos][1],self.start_z-48,0)
        self.move_increment(0,0,-10)
        self.succ(True)
        self.move_increment(0,0,40)
        self.move_to(positions[stack][0],positions[stack][1],height+30,0)
        self.move_increment(0,0,-40)
        self.succ(False)
        self.move_increment(0,0,30)
        self.go_home()
        
        size+=1
        
        if color == "r":
            self.red_stack=size
        else:
            self.blue_stack=size
    
    def calibHeight(self):
        self.move_increment(0,0,80) #move to z height of 70 (from the ground)
    
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

    def goToPos(self,position):
        pos = self.positions[position]
        self.move_to(pos[0],pos[1],self.start_z-60,0)
        
    def setHome(self):
        self.start_x = self.dobot.pose()[0]
        self.start_y = self.dobot.pose()[1]
        self.start_z = self.dobot.pose()[2]
        
        x = self.start_x
        y = self.start_y
        
        self.positions = (
                    (x+30,y-25), #squares 1-9
                    (x+30,y+5),
                    (x+30,y+40),
                    (x+65,y-30),
                    (x+65,y+5),
                    (x+65,y+40),
                    (x+100,y-30),
                    (x+100,y+5),
                    (x+100,y+40),
                    (x+65,y+90), #red stack
                    (x+60,y-90), #blue  
                    (x,y))
        return (self.start_x,self.start_y,self.start_z)
        


