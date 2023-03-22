import pydobot

class DobotBot:

    def __init__(self,port):
        self.dobot = pydobot.Dobot(port)
        self.start_x = 0
        self.start_y = 150
        self.start_z = 0

    def move_bot(self,siit,sinna):
        if siit == 10:
            Z = red_stack * 24 + z_offset
        if siit == 11:
            Z = blue_stack * 24 + z_offset
        else: Z = 24 + z_offset

    def calibrate(self, x, y, z):
        self.start_x = x
        self.start_y = y
        self.start_z = z

        positions = (
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


