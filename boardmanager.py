import copy
import math
import random


X = "r"
O = "b"
EMPTY = None

class Board():
    def __init__(self):# Initializing the board
    
        self.board = [[EMPTY, EMPTY, EMPTY],
                     [EMPTY, EMPTY, EMPTY],
                     [EMPTY, EMPTY, EMPTY]]
    
    
    def player(self, board):
        """
        Returns player who has the next turn on a board.
        """
        count = 0
        for i in board:
            for j in i:
                if j:
                    count += 1
        if count % 2 != 0:
            return O
        return X
    
    
    def actions(self, board):
        """
        Returns set of all possible actions (i, j) available on the board.
        """
        res = set()
        board_len = len(board)
        for i in range(board_len):
            for j in range(board_len):
                if board[i][j] == EMPTY:
                    res.add((i, j))
        return res
    
    
    def result(self, board, action):
        """
        Returns the board that results from making move (i, j) on the board.
        """
        curr_player = self.player(board)
        result_board = copy.deepcopy(board)
        (i, j) = action
        result_board[i][j] = curr_player
        return result_board
    
    
    def get_horizontal_winner(self, board):
        # check horizontally
        winner_val = None
        board_len = len(board)
        for i in range(board_len):
            winner_val = board[i][0]
            for j in range(board_len):
                if board[i][j] != winner_val:
                    winner_val = None
            if winner_val:
                return winner_val
        return winner_val
    
    
    def get_vertical_winner(self, board):
        # check vertically
        winner_val = None
        board_len = len(board)
        for i in range(board_len):
            winner_val = board[0][i]
            for j in range(board_len):
                if board[j][i] != winner_val:
                    winner_val = None
            if winner_val:
                return winner_val
        return winner_val
    
    
    def get_diagonal_winner(self, board):
        # check diagonally
        winner_val = None
        board_len = len(board)
        winner_val = board[0][0]
        for i in range(board_len):
            if board[i][i] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    
        winner_val = board[0][board_len - 1]
        for i in range(board_len):
            j = board_len - 1 - i
            if board[i][j] != winner_val:
                winner_val = None
    
        return winner_val
    
    
    def winner(self, board):
        """
        Returns the winner of the game, if there is one.
        """
        winner_val = self.get_horizontal_winner(board) or self.get_vertical_winner(board) or self.get_diagonal_winner(board) or None
        return winner_val
    
    
    def terminal(board):
        """
        Returns True if game is over, False otherwise.
        """
        if self.winner(board) != None:
            return True
    
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
        return True
    
    def utility(self, board):
        """
        Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        """
        winner_val = self.winner(board)
        if winner_val == X:
            return 1
        elif winner_val == O:
            return -1
        return 0
    
    def max_value(self, board):
        if self.terminal(board):
            return self.utility(board), None
    
        v = float('-inf')
        move = None
        for action in self.actions(board):
            x, _ = self.min_value(self.result(board, action))
            if x > v:
                v = x
                move = action
                if v == 1:
                    return v, move
    
        return v, move
    
    
    def min_value(self, board):
        if self.terminal(board):
            return self.utility(board), None
    
        v = float('inf')
        move = None
        for action in self.actions(board):
            x, _ = self.max_value(self.result(board, action))
            if x < v:
                v = x
                move = action
                if v == -1:
                    return v, move
    
        return v, move
    
    def minimax(self, board):
        """
        Returns the optimal action for the current player on the board.
        """
        if self.terminal(board):
            return None
        else:
            if self.player(board) == X:
                _, move = self.max_value(board)
                return move
            else:
                _, move = self.min_value(board)
                return move
      
    def print_board(self, board):
        print("\n")
        for row in board:
            print(row, )
            
        print("\n")
    
    def set_board(self,board):
        """
        Set the board of the game (if u want to for example fetch the board from gsheets)
        """
        self.board = board
    
    def make_move(self,side,move):
        """
        Place a block of a player (r or b) in a slot 0-8
        """
        #needs to be implemented
        
    
    #if __name__ == "__main__":
    #    board = [[X, O, EMPTY],
    #            [X, O, EMPTY],
    #            [EMPTY, EMPTY, EMPTY]]
    
        #move = minimax(board)
        #print(move)