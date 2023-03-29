import pydobot

class DobotBot:

    def __init__(self,port):
        self.dobot = pydobot.Dobot(port)
        self.start_x = 0
        self.start_y = 150
        self.start_z = 0

    def move_bot(self,siit,sinna):
        if siit == 10:
            z = red_stack * 24 + self.start_z
            red_stack -= 1
        if siit == 11:
            z = blue_stack * 24 + self.start_z
            blue_stack -= 1
        else: z = 24 + self.start_z
        
        self.go_home()
        self.dobot.move_to(self.positions[siit][0], self.positions[siit][1], z, 0)
        self.dobot.suck(1)
        self.go_home()
        self.dobot.move_to(self.positions[sinna][0], self.positions[sinna][1], z, 0)
        self.dobot.suck(0)
        self.go_home()



    def calibrate(self, x, y, z):
        self.start_x = x
        self.start_y = y
        self.start_z = z

        self.positions = (
                    (x,y),
                    (x,y+35),
                    (x,y+70),
                    (x+35,y),
                    (x+35,y+35),
                    (x+35,y+70),
                    (x+70,y),
                    (x+70,y+35),
                    (x+70,y+70)
                    )

    def go_home(self):
        self.dobot.move_to(230, 0, 70, 0)

# 255 -35 -71


