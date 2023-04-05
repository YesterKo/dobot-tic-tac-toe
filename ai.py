#the unused cousin of the minimax.py
#Storing the game gamestate
#|0|1|2|
#|3|4|5|
#|6|7|8|
# o - empty space
# b - blue's move (analog is o)
# r - red's move (analog is x, goes first)
class ai():
	def __init__(self,side):
		self.side = side #side blue or red
		self.victorystates = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]# all victory states, there are 8 in total so no need for complicated stuff
	def calcScore(self,move):
		enemy = "b"
		if self.side=="b":
			enemy = "r"
			
		for i in self.victorystates:
			if (gamestate[i[0]]==enemy and gamestate[i[1]]==enemy and gamestate[i[2]]==enemy):
				return -1 
			elif (gamestate[i[0]]==self.side and gamestate[i[1]]==self.side and gamestate[i[2]]==self.side):
				return 1
			else:
				return calcScore()
						
	def bestMove(self, gamestate): 
		availables = [] #available moves
		enemy = "b"
		if self.side=="b":
			enemy = "r"
			
		for i in self.victorystates:
			if (gamestate[i[0]]==enemy and gamestate[i[1]]==enemy and gamestate[i[2]]==enemy):
				return -1 #code retWzurns move to make, if move is -1, game is over
			
		for i in range(len(gamestate)):
			if gamestate[i] == "o":
				availables.append(i)
		scores = []
		map(calcScore,availables)
			
		
	
				
				
				