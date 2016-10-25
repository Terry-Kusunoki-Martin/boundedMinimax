########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from Players import *
from HexGame import *
from random import choice

class Node(object):
    """Node used in minimax search"""
    def __init__(self, board, move, depth, side):
        self.board = board
        self.move = move # move that got us here
        self.depth = depth
        self.side = side # +1 for black, or -1 for white

class BoundedMinimaxPlayer(Player):
  #TODO: test expansionscore with print statements
    """Uses depth-bounded minimax to choose a move"""
    def __init__(self, game, depthLimit, boardEval="basicEval", name=None):
        if name == None:
            name = "BoundedMinimax-Depth"+str(depthLimit)
        Player.__init__(self, name)
        self.boardEval = eval("self."+boardEval)#set self.boardEval to self.?
        self.game = game
        self.depthLimit = depthLimit
        self.bestMove = None

    def basicEval(self, board):
        """Black is the maximizer, so we want positive scores when board is
        good for black and negative scores when board is good for
        white. Should return highest score when black wins. Should
        return lowest score when white wins.  Otherwise should return
        number of black's connected pieces minus the number of white's
        connected pieces."""
        if self.game.blackWins(board):
            return self.game.size ** 3
        elif self.game.whiteWins(board):
            return (-1 * (self.game.size ** 3))
        else:
            return self.game.countConnected(board, self.side)

    def testEval(self, board):
        if self.game.blackWins(board):
            return self.game.size ** 3
        elif self.game.whiteWins(board):
            return (-1 * (self.game.size ** 3))
        else:
            return (self.game.betterCountConnected(board, self.side) + self.game.expansionScore(board, self.side))

    def betterEval(self, board):
        """Invent a better evaluator than the one above.
        count virtually won boards the same as winning boards
        higher scores for expanding to a row/col that hasn't yet been occupied by the color
        place at center for first move
        for first few moves, placing pieces w gap of 1 has higher score
        djust countconnected to take side into account, and only count nodes connected in the correct direction
        """
        
        moves_made = self.game.size ** 2 - len(self.game.getPossibleMoves(board))
        if moves_made <= 2:#prefer boards where piece is placed in the middle for turn 1
            reference = self.game.size/2
            if self.game.size % 2 == 0:
                board1 = board[reference, reference]
                board2 = board[reference - 1, reference]
                board3 = board[reference, reference - 1]
                board4 = board[reference - 1, reference - 1]
                if self.side == -1 and -1 in [board1, board2, board3, board4]:
                  return -1 * (self.game.size ** 3)
                elif self.side == 1 and 1 in [board1, board2, board3, board4]:
                  return self.game.size ** 3

            if self.game.size % 2 == 1:

                board1 = board[reference, reference] 
                board2 = board[reference - 1, reference] 
                board3 = board[reference + 1, reference] 
                board4 = board[reference, reference - 1] 
                board5 = board[reference, reference + 1] 
                if self.side == -1 and -1 in [board1, board2, board3, board4, board5]:
                  return -1 * (self.game.size ** 3)
                elif self.side == 1 and 1 in [board1, board2, board3, board4, board5]:
                  return self.game.size ** 3

        if self.side == -1:
            adjuststage = 1
        else:
            adjuststage = 0

        if moves_made > 2 and moves_made <= self.game.size + adjuststage:#prefer fast expansion in early stage of game
            
            return (self.game.countConnectedGap(board, self.side) + self.game.expansionScore(board, self.side))

        if self.game.blackWins(board):
            return self.game.size ** 3
        elif self.game.whiteWins(board):
            return (-1 * (self.game.size ** 3))
        else:
            return (self.game.betterCountConnected(board, self.side) + self.game.expansionScore(board, self.side))

       



    def boundedMinimax(self, node):
        if node.depth == self.depthLimit:
            return self.boardEval(node.board)
        possiblemoves = self.game.getPossibleMoves(node.board)
        if len(possiblemoves) == 0:
            return self.boardEval(node.board)
        scores = []
        
        for move in possiblemoves:
            nextBoard = self.game.getNextBoard(node.board, move, self.side)
            nextNode = Node(nextBoard, move, node.depth + 1, self.side * -1)
            scores.append(self.boundedMinimax(nextNode))
            
        if self.side == 1:
            if node.depth == 0:
                m = max(scores)
                ilist = [i for i, j in enumerate(scores) if j == m]
                self.bestMove = possiblemoves[choice(ilist)]
            return max(scores)
        else:
            if node.depth == 0:
                m = min(scores)
                ilist = [i for i, j in enumerate(scores) if j == m]
                self.bestMove = possiblemoves[choice(ilist)]
            return min(scores)

    def getMove(self, board):
        """Performs depth-limited minimax search to select a move.
        Returns the best move on the current board
        the best move found from the root node at depth 0.
        Should create a node for the current board state and then call a
        recursive helper function that performs minimax"""        
        self.boundedMinimax(Node(board, None, 0, self.side))
        return self.bestMove



    

class AlphaBetaPruningPlayer(BoundedMinimaxPlayer):

    def ab_Minimax(self, node, alpha=float("-inf"), beta=float("inf")):
        if node.depth == self.depthLimit or self.game.whiteWins(node.board) or self.game.blackWins(node.board):
            return self.boardEval(node.board)
        if node.side == 1:
            v = float("-inf")
        else:
            v = float("inf")
        
        possiblemoves = self.game.getPossibleMoves(node.board)
        if len(possiblemoves) == 0:
            return self.boardEval(node.board)

        if node.depth == 0:
            scores = []
        
        bestmoves = []
        
        for moves in range(len(possiblemoves)):
            move = possiblemoves[moves]
            nextBoard = self.game.getNextBoard(node.board, move, self.side)
            nextNode = Node(nextBoard, move, node.depth + 1, self.side * -1)
            if node.side == 1:
                result = self.ab_Minimax(nextNode, alpha, beta)
                if result > v:
                    v = result
                    bestmoves = [moves]
                elif result == v:
                    bestmoves.append(moves)
                if node.depth == 0:
                    scores.append(v)

                if v > beta:
                    return v
                alpha = max(v, alpha)
            else:
                result = self.ab_Minimax(nextNode, alpha, beta)
                if result < v:
                    v = result
                    bestmoves = [moves]
                elif result == v:
                    bestmoves.append(moves)
                if node.depth == 0:
                    scores.append(v)
                if v < alpha:
                    return v
                beta = min(v, beta)

        if node.depth == 0:
            self.bestMove = possiblemoves[choice(bestmoves)]
                    
        return v




    
    def getMove(self, board):
        """Performs depth-limited minimax search with Alpha-Beta pruning.
        Alpha-Beta minimax works similarly to boundedMinimax, but cuts off
        search down branches that cannot lead to better outcomes."""
        
        self.ab_Minimax(Node(board, None, 0, self.side), float("-inf"), float("inf"))
        return self.bestMove
