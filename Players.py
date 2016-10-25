########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from random import choice, shuffle

class Player(object):
    """A base class for Hex players.  All players must implement the
    getMove method."""
    def __init__(self, name=None):
        self.name = name
        self.side = None
        self.game = None
        self.wins = 0
        self.losses = 0
    def setSide(self, side):
        self.side = side
    def otherSide(self, side):
        return -1*side
    def won(self):
        self.wins += 1
    def lost(self):
        self.losses += 1
    def results(self):
        result = self.name + ": "
        result += str(self.wins) + " wins, " 
        result += str(self.losses) + " losses"
        return result
    def getMove(self, board):
        """
        Given the current board, should return a valid move.
        """
        raise NotImplementedError()

class RandomPlayer(Player):
    """Selects a random choice move."""
    def __init__(self, game, name="RandomPlayer"):
        Player.__init__(self, name)
        self.game = game
    def getMove(self, board):
        return choice(self.game.getPossibleMoves(board))

class HumanPlayer(Player):
    """Selects a move chosen by the user."""
    def __init__(self, game, name="HumanPlayer"):
        Player.__init__(self, name)
        self.game = game
    def getMove(self, board):
        print("\n%s's turn" % (self.name))
        while True:
            row = None
            col = None
            while row == None or col == None:
                try:
                    row, col = input("Enter row, col: ")
                except Exception:
                    print "Couldn't parse input; try again."
                    continue
            if row >= self.game.size or col >= self.game.size or \
               row < 0 or col < 0:
                print("Invalid move: row and col must be on board")
            elif self.game.board[row,col] != 0:
                print("Invalid move: there is already a piece there")
            else:
                return (row, col)
