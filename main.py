from camera import cameraMan
from dobot_driver import DobotBot
import keyboard
import minimax
import time
import cv2

print("------------Welcome to dobot tic-tac-toe------------")
print("Please select the gamemode:")
print("Physical mode - place blocks by hand in the real world")
print("Virtual mode - place blocks in the sheet and the robot moves the blocks onto the board")
physical = True #if input("Physical or virtual? ").upper()=="Physical".upper() else False
print(physical)

cam = cameraMan()
dobot = DobotBot("/dev/ttyUSB1")

initializing = True
print("Please align the robot to so the suction cup is on the playing field in the middle below the grid")
print("After you're done, press space")
cam.startCam(False)
while initializing:
	camera = cam.getCam("img")
	if camera is not None:
			if camera.shape[0] > 0:
				cv2.imshow("img",camera)
				if cv2.waitKey(1) & 0xFF==ord('q'):
					exit()
	if keyboard.is_pressed("space"):
		initializing = False

dobot.calibHeight()
print("Successfully initalized!")
print("Calibrating...")



calibrating = True
while calibrating:
	print("Current offset:","X:",cam.getOffset()[1],"Y:",cam.getOffset()[0],)
	camera = cam.getCam("img")
	if camera is not None:
		if camera.shape[0] > 0:
			cv2.imshow("img",camera)
	if cv2.waitKey(1) & 0xFF==ord('q'):
		exit()
	dobot.calibrate(cam.getOffset()[1],cam.getOffset()[0])
	if cam.getOffset()[0]>-2 and cam.getOffset()[0]<2 and cam.getOffset()[1]>-2 and cam.getOffset()[1]<2:
		print("Succesfully calibrated!")
		calibrating = False
		dobot.setHome()


if physical:
	camera = cam.getCam("img")
	blue = cam.getCam("blue_out")
	red = cam.getCam("red_out")
	running = True
	while running: #idk if this is the correct way of doing this, but it doesn't matter that much
		cv2.imshow("img",camera)
		cv2.imshow("blue",blue)
		cv2.imshow("red",red)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			exit()
		