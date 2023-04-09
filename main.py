from camera import cameraMan
from dobot_driver import DobotBot
import minimax


print("------------Welcome to dobot tic-tac-toe------------")
print("Please select the gamemode:")
print("Physical mode - place blocks by hand in the real world")
print("Virtual mode - place blocks in the sheet and the robot moves the blocks onto the board")
physical = True #if input("Physical or virtual? ").upper()=="Physical".upper() else False
print(physical)

cam = cameraMan()
if physical:
	cam.startCam(True,False)
	print("Hwwy")
	while True:
		print(cam.getOffset())