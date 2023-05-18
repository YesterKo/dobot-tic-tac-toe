from camera import CameraMan
from dobot_driver import DobotBot
from sheets_com import Sheet
from boardmanager import Board
from copy import deepcopy
import keyboard
import cv2

print("------------Welcome to dobot tic-tac-toe------------")
print("Please select the gamemode:")
print("Physical mode - place blocks by hand in the real world")
print("Virtual mode - place blocks in the sheet and the robot moves the blocks onto the board")
physical = False #if input("Physical or virtual? ").upper()=="Physical".upper() else False
print(physical)

#cam = CameraMan()
#dobot = DobotBot("/dev/ttyUSB0")

calib = False

coords = [0,0,0]
with open("coords.txt","r") as file:
    lines = file.readlines()
    if len(lines)>2:
        coords[0] = float(lines[0])
        coords[1] = float(lines[1])
        coords[2] = float(lines[2])
    else:
        calib = True

print(coords)
#cam.startCam(False)

if not calib:
    if input("Do you want to calibrate again? ").lower() == "yes":
        calib = True

if calib:
    initializing = True
    print("Please align the robot to so the suction cup is on the playing field in the middle below the grid")
    print("After you're done, press space")
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
            coords = dobot.setHome()
            with open("coords.txt","w") as file:
                file.writelines([str(i)+"\n" for i in coords])

else:
    print("bro")
    #dobot.dobot.move_to(coords[0],coords[1],coords[2],0,wait=True)
    #dobot.setHome()    

print("The robot will now proceed to go to the position of each square.")
print("Please confirm that the square locations are correct and if nescessary, recalibrate")

#for i in range(12):
#    dobot.goToPos(i)
#dobot.go_home()

print("Place the blocks and press space")
placing = True
while placing:
    if keyboard.is_pressed("space"):
            placing = False
        
        
sheet = Sheet("1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA","Sheet1")
boardman = Board()

if physical:
    running = True
    
    while running: #idk if this is the correct way of doing this, but it doesn't matter that much
        camera = cam.getCam("img")
        blue = cam.getCam("blue_out")
        red = cam.getCam("red_out")
        cv2.imshow("img",camera)
        cv2.imshow("blue",blue)
        cv2.imshow("red",red)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            exit()
else:
    while True:
        input("Press enter to get data from google sheets and place the required blocks")
        
        data = sheet.get_data_from_sheet()
        print(data)
        data = [[ None if e == "nan" else e for e in i ] for i in data] #replace nan with None
        print(data)
        
        old_board = deepcopy(boardman.board)
        boardman.set_board(data)
        new_board = data
        
        boardman.print_board(old_board)
        boardman.print_board(data)
        
        count = 0
        
        to_remove = []
        to_place = []
         
        for i in range(len(old_board)):
            for e in range(len(old_board[i])):
                if old_board[i][e]!=new_board[i][e]:
                    if old_board[i][e] != None:
                        to_remove.append((old_board[i][e],count))
                    if new_board[i][e]!=None: 
                        to_place.append((new_board[i][e],count))
                count+=1
        
        for block in to_remove:
        #    dobot.remove_block(block[0],block[1])
            print("removing: ",block)
        
        for block in to_place:
        #    dobot.place_block(block[0],block[1])
            print("placing: ",block)
    
        
    #print("lmao")
    
    #dobot.place_block("r",4)
    #dobot.place_block("r",2)
    #dobot.place_block("r",6)
    #dobot.place_block("r",0)
    #dobot.place_block("r",8)
    #dobot.place_block("b",4)
    #dobot.place_block("b",2)
    #dobot.place_block("b",6)
    #dobot.place_block("b",0)
    #dobot.place_block("b",8)
    