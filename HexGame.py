#! /usr/bin/env python
########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from Queues import FIFO_Queue
from copy import deepcopy
from Players import *
import numpy as np
from sys import argv
from Minimax import *

def main():
    if len(argv) > 1:
        size = int(argv[1])
    else:
        size = 8
    game = HexGame(size)
    p1 = AlphaBetaPruningPlayer(game, 1, "betterEval")
    p2 = RandomPlayer(game)
    game.playOneGame(p1, p2)

def print_char(i):
    if i > 0:
        return u'\u25CB' # black piece
    if i < 0:
        return u'\u25CF' # white piece
    return u'\u00B7' # empty cell


class HexGame(object):
    def __init__(self, size):
        """The board is represented as an array of integers with dimension
        size x size. Blank cellse are represented by 0; cells with a piece
        are represented by 1 for black or -1 for white."""
        self.size = size
        self.reset()

    def reset(self):
        """Resets the board to the starting configuration."""
        self.board = np.zeros([self.size, self.size], int)
        self.turn = 1 # +1 for black; -1 for white

    def toStr(self):
        result = u"\n" + (" " + u"\u25a0")*self.size + u" \u25E9\n"
        for i in range(self.size):
            result += " " * i + u"\u25A1" + " "
            for j in range(self.size):
                result += print_char(self.board[i,j]) + " "
            result += u"\u25A1" + "\n"
        result += " "*(self.size) + u"\u25EA" + (" " + u"\u25a0") * self.size
        return result

    def playOneGame(self, player1, player2, show=True):
        """Plays a game and returns winner."""
        self.reset()
        player1.setSide(1)
        player2.setSide(-1)
        if show:
            print("%s vs %s" % (player1.name, player2.name))
        while True:
            if self.turn > 0:
                cur_player = player1
            else:
                cur_player = player2
            if show:
                print self.toStr()
                print cur_player.name + "'s turn to place a " + \
                        print_char(cur_player.side) + " piece"
            row, col = cur_player.getMove(self.board)
            self.board[row][col] = self.turn
            
            if show:
                print("Made move (%d, %d)" % (row, col))
            if self.turn > 0 and self.blackWins(self.board):
                break
            elif self.turn < 0 and self.whiteWins(self.board):
                break
            self.turn *= -1
        if show:
            print self.toStr()
            print cur_player.name + " wins"
        return self.turn

    def playNGames(self, n, player1, player2, show=False):
        """
        Will play out n games between player1 and player2.
        The players alternate going first.  Prints the total
        number of games won by each player.
        """
        first = player1
        second = player2
        for i in range(n):
            if show:
                print "Game", i
            winner = self.playOneGame(first, second, show)
            if winner > 0:
                first.won()
                second.lost()
                if show:
                    print first.name, "wins"
            else:
                first.lost()
                second.won()
                if show:
                    print second.name, "wins"
            first, second = second, first
        print first.results()
        print second.results()

    def getPossibleMoves(self, board):
        """Returns a list of all possible moves on the given board."""
        possible = []
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    possible.append((row, col))
        return possible

    def getNextBoard(self, board, move, player):
        """Returns a new board showing how the given board would look after
        the move by player."""
        row, col = move
        if board[row][col] != 0:
            print("Error invalid move: %s" % (move))
            exit()
        nextBoard = deepcopy(board)
        nextBoard[row][col] = player
        return nextBoard

    def getNeighbors(self, row, col):
        """Returns a list of neighboring cells to the given row and col."""
        ls = []
        if row > 0:
            ls.append((row-1, col))
        if row < self.size-1:
            ls.append((row+1, col))
        if col > 0:
            ls.append((row, col-1))
        if col < self.size-1:
            ls.append((row, col+1))
        if row > 0 and col < self.size-1:
            ls.append((row-1, col+1))
        if row < self.size-1 and col > 0:
            ls.append((row+1, col-1))
        return ls
 
    def getNeighborsGap(self, row, col, side):
        """Returns a list of neighbors one row/col away from the original pt."""
        ls = []
        if side == 1:#we only care about right and left
            if col > 1:
                ls.append((row, col - 2, 1))
                if row < self.size - 1:
                    ls.append((row + 1, col - 2, 2))
                if row < self.size - 2:
                    ls.append((row + 2, col - 2, 1))
            
            if col < self.size - 2:
                ls.append((row, col + 2, 1))
                if row >= 1:
                    ls.append((row - 1, col + 2, 2))
                if row >= 2:
                    ls.append((row - 2, col + 2, 1))

        else:#we only care about up and down
            if row > 1:
                ls.append((row - 2, col, 1))
                if col < self.size - 1:
                    ls.append((row - 2, col + 1, 2))
                if col < self.size - 2:
                    ls.append((row - 2, col + 2, 1))
            if row < self.size - 2:
                ls.append((row + 2, col, 1))
                if col >= 1:
                    ls.append((row + 2, col - 1, 2))
                if col >= 2:
                    ls.append((row + 2, col - 2, 1))
                
        return ls

 
    def getRelevantNeighbors(self, row, col, side):
        """Returns a pared down list of neighbors depending on side"""
        ls = []
        if side == 1:#we only care about right and left
            if col >= 1:
                ls.append((row, col - 1))
                if row < self.size - 1:
                    ls.append((row + 1, col - 1))
            
            if col < self.size - 1:
                ls.append((row, col + 1))
                if row >= 1:
                    ls.append((row - 1, col + 1))

        else:#we only care about up and down
            if row >= 1:
                ls.append((row - 1, col))
                if col < self.size - 1:
                    ls.append((row - 1, col + 1))
            if row < self.size - 1:
                ls.append((row + 1, col))
                if col >= 1:
                    ls.append((row + 1, col - 1))
                
        return ls


    def blackWins(self, board):
        """Returns True if black player wins, otherwise False."""
        queue = FIFO_Queue()
        visited = set()
        # Add all locations of black pieces in the leftmost col to queue
        for row in range(self.size):
            if board[row][0] == 1:
                queue.add((row, 0))
        # Try to find a path to the rightmost col
        while len(queue) > 0:
            row, col = queue.get()
            visited.add((row, col))
            for n in self.getNeighbors(row, col):
                r, c = n
                if board[r][c] != 1: continue
                if c == self.size-1: return True
                if n in visited or n in queue:
                    continue
                queue.add(n)
        return False

    def whiteWins(self, board):
        """Returns True if white player wins, otherwise False."""
        queue = FIFO_Queue()
        visited = set()
        # Add all locations of white pieces n the top row to queue
        for col in range(self.size):
            if board[0][col] == -1:
                queue.add((0, col))
        # Try to find a path to the bottom row
        while len(queue) > 0:
            row, col = queue.get()
            visited.add((row, col))
            for n in self.getNeighbors(row, col):
                r, c = n
                if board[r][c] != -1: continue
                if r == self.size-1: return True
                if n in visited or n in queue:
                    continue
                queue.add(n)
        return False

    def countConnected(self, board, side):
        """Counts how many pieces for the given side touch another piece
        of the same side."""
        queue = FIFO_Queue()
        counted = set()
        acc = 0
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == side:
                    queue.add((row, col))
        while len(queue) > 0:
            row, col = queue.get()
            for n in self.getNeighbors(row, col):
                r, c = n
                if board[r][c] == side and n not in counted:
                    counted.add((r, c))
                    acc += 1
                    
        return (acc * side)

    def betterCountConnected(self, board, side):
        """Counts how many pieces for the given side touch another piece
        of the same side."""
        queue = FIFO_Queue()
        counted = set()
        acc = 0
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == side:
                    queue.add((row, col))
        
        while len(queue) > 0:
            row, col = queue.get()
            for n in self.getRelevantNeighbors(row, col, side):
                r, c = n
                if board[r][c] == side and n not in counted:
                    counted.add((r, c))
                    acc += 1
                    
        return (acc * side)


    def countConnectedGap(self, board, side):
        """Counts how many pieces for the given side touch another piece
        of the same side."""
        queue = FIFO_Queue()
        counted = set()
        acc = 0
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == side:
                    queue.add((row, col))

        while len(queue) > 0:
            row, col = queue.get()
            for n in self.getNeighborsGap(row, col, side):
                r, c, s = n
                if board[r][c] == side and (r, c) not in counted:
                    counted.add((r, c))
                    acc += s

                    
        return (acc * side)

    def expansionScore(self, board, side):

        if side == 1:
            colsExpanded = set()
            for row in range(self.size):
                for col in range(self.size):
                    if col in colsExpanded:
                        continue
                    if board[row][col] == side:
                        colsExpanded.add(col)
            return len(colsExpanded)
        
        if side == -1:
            rowsExpanded = set()
            for row in range(self.size):
                if row in rowsExpanded:
                    continue
                for col in range(self.size):
                    if board[row][col] == side:
                        rowsExpanded.add(row)
            return len(rowsExpanded) * -1
               

            

if __name__ == '__main__':
    main()
