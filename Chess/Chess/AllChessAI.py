import random
import time
import numpy as np

# pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
# checkmate = 1000
# stalemate = 0
# DEPTH = 3
#
# knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 2, 2, 2, 2, 2, 2, 1],
#                 [1, 2, 3, 3, 3, 3, 2, 1],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [1, 2, 3, 3, 3, 3, 2, 1],
#                 [1, 2, 2, 2, 2, 2, 2, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1]]
#
# bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
#                 [3, 4, 3, 2, 2, 3, 4, 3],
#                 [2, 3, 4, 3, 3, 4, 3, 2],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [2, 3, 4, 3, 3, 4, 3, 2],
#                 [3, 4, 3, 2, 2, 3, 4, 3],
#                 [4, 3, 2, 1, 1, 2, 3, 4]]
#
# queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
#                [1, 2, 3, 3, 3, 1, 1, 1],
#                [1, 4, 3, 3, 3, 4, 2, 1],
#                [1, 2, 3, 3, 3, 2, 2, 1],
#                [1, 2, 3, 3, 3, 2, 2, 1],
#                [1, 4, 3, 3, 3, 4, 2, 1],
#                [1, 1, 2, 3, 3, 1, 1, 1],
#                [1, 1, 1, 3, 1, 1, 1, 1]]
#
# rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
#               [4, 4, 4, 4, 4, 4, 4, 4],
#               [1, 1, 2, 3, 3, 2, 1, 1],
#               [1, 2, 3, 4, 4, 3, 2, 1],
#               [1, 2, 3, 4, 4, 3, 2, 1],
#               [1, 1, 2, 3, 3, 2, 1, 1],
#               [4, 4, 4, 4, 4, 4, 4, 4],
#               [4, 3, 4, 4, 4, 4, 3, 4]]
#
# whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
#                    [8, 8, 8, 8, 8, 8, 8, 8],
#                    [5, 6, 6, 7, 7, 6, 6, 5],
#                    [2, 3, 3, 5, 5, 3, 3, 2],
#                    [1, 2, 3, 4, 4, 3, 2, 1],
#                    [1, 1, 2, 3, 3, 2, 1, 1],
#                    [1, 1, 1, 0, 0, 1, 1, 1],
#                    [0, 0, 0, 0, 0, 0, 0, 0]]
#
# blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
#                    [1, 1, 1, 0, 0, 1, 1, 1],
#                    [1, 1, 2, 3, 3, 2, 1, 1],
#                    [1, 2, 3, 4, 4, 3, 2, 1],
#                    [2, 3, 3, 5, 5, 3, 3, 2],
#                    [5, 6, 6, 7, 7, 6, 6, 5],
#                    [8, 8, 8, 8, 8, 8, 8, 8],
#                    [8, 8, 8, 8, 8, 8, 8, 8]]

pieceScore = {'K': 20000, 'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'p': 100}
checkmate = 100000
stalemate = 0
DEPTH = 3
MAXDURATION = 5   # time given to AI to run in seconds

whiteKnightScores = np.array([[-50,-40,-30,-30,-30,-30,-40,-50],
                     [-40,-20,  0,  0,  0,  0,-20,-40],
                     [-30,  0, 10, 15, 15, 10,  0,-30],
                     [-30,  5, 15, 20, 20, 15,  5,-30],
                     [-30,  0, 15, 20, 20, 15,  0,-30],
                     [-30,  5, 10, 15, 15, 10,  5,-30],
                     [-40,-20,  0,  5,  5,  0,-20,-40],
                     [-50,-40,-30,-30,-30,-30,-40,-50]])

blackKnightScores = np.array([[-50,-40,-30,-30,-30,-30,-40,-50],
                     [-40,-20,  0,  5,  5,  0,-20,-40],
                     [-30,  5, 10, 15, 15, 10,  5,-30],
                     [-30,  0, 15, 20, 20, 15,  0,-30],
                     [-30,  5, 15, 20, 20, 15,  5,-30],
                     [-30,  0, 10, 15, 15, 10,  0,-30],
                     [-40,-20,  0,  0,  0,  0,-20,-40],
                     [-50,-40,-30,-30,-30,-30,-40,-50]])

whiteBishopScores = np.array([[-20,-10,-10,-10,-10,-10,-10,-20],
                     [-10,  0,  0,  0,  0,  0,  0,-10],
                     [-10,  0,  5, 10, 10,  5,  0,-10],
                     [-10,  5,  5, 10, 10,  5,  5,-10],
                     [-10,  0, 10, 10, 10, 10,  0,-10],
                     [-10, 10, 10, 10, 10, 10, 10,-10],
                     [-10,  5,  0,  0,  0,  0,  5,-10],
                     [-20,-10,-10,-10,-10,-10,-10,-20]])

blackBishopScores = np.array([[-20,-10,-10,-10,-10,-10,-10,-20],
                     [-10,  5,  0,  0,  0,  0,  5,-10],
                     [-10, 10, 10, 10, 10, 10, 10,-10],
                     [-10,  0, 10, 10, 10, 10,  0,-10],
                     [-10,  5,  5, 10, 10,  5,  5,-10],
                     [-10,  0,  5, 10, 10,  5,  0,-10],
                     [-10,  0,  0,  0,  0,  0,  0,-10],
                     [-20,-10,-10,-10,-10,-10,-10,-20]])

whiteQueenScores = np.array([[-20,-10,-10, -5, -5,-10,-10,-20],
                    [-10,  0,  0,  0,  0,  0,  0,-10],
                    [-10,  0,  5,  5,  5,  5,  0,-10],
                    [ -5,  0,  5,  5,  5,  5,  0, -5],
                    [  0,  0,  5,  5,  5,  5,  0, -5],
                    [-10,  5,  5,  5,  5,  5,  0,-10],
                    [-10,  0,  5,  0,  0,  0,  0,-10],
                    [-20,-10,-10, -5, -5,-10,-10,-20]])

blackQueenScores = np.array([[-20,-10,-10, -5, -5,-10,-10,-20],
                    [-10,  0,  5,  0,  0,  0,  0,-10],
                    [-10,  5,  5,  5,  5,  5,  0,-10],
                    [  0,  0,  5,  5,  5,  5,  0, -5],
                    [ -5,  0,  5,  5,  5,  5,  0, -5],
                    [-10,  0,  5,  5,  5,  5,  0,-10],
                    [-10,  0,  0,  0,  0,  0,  0,-10],
                    [-20,-10,-10, -5, -5,-10,-10,-20]])

whiteRookScores = np.array([[  0,  0,  0,  0,  0,  0,  0,  0],
                   [  5, 10, 10, 10, 10, 10, 10,  5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [  0,  0,  0,  5,  5,  0,  0,  0]])

blackRookScores = np.array([[  0,  0,  0,  5,  5,  0,  0,  0],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [ -5,  0,  0,  0,  0,  0,  0, -5],
                   [  5, 10, 10, 10, 10, 10, 10,  5],
                   [  0,  0,  0,  0,  0,  0,  0,  0]])

whitePawnScores = np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
                   [50, 50, 50, 50, 50, 50, 50, 50],
                   [10, 10, 20, 30, 30, 20, 10, 10],
                   [ 5,  5, 10, 25, 25, 10,  5,  5],
                   [ 0,  0,  0, 20, 20,  0,  0,  0],  #
                   [ 5, -5,-10,  0,  0,-10, -5,  5],
                   [ 5, 10, 10,-40,-40, 10, 10,  5],
                   [ 0,  0,  0,  0,  0,  0,  0,  0]])

blackPawnScores = np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
                   [ 5, 10, 10,-40,-40, 10, 10,  5],
                   [ 5, -5,-10,  0,  0,-10, -5,  5],
                   [ 0,  0,  0, 20, 20,  0,  0,  0],
                   [ 5,  5, 10, 25, 25, 10,  5,  5],
                   [10, 10, 20, 30, 30, 20, 10, 10],
                   [50, 50, 50, 50, 50, 50, 50, 50],
                   [ 0,  0,  0,  0,  0,  0,  0,  0]])

whiteKingScores = np.array([[-30,-40,-40,-50,-50,-40,-40,-30],
                   [-30,-40,-40,-50,-50,-40,-40,-30],
                   [-30,-40,-40,-50,-50,-40,-40,-30],
                   [-30,-40,-40,-50,-50,-40,-40,-30],
                   [-20,-30,-30,-40,-40,-30,-30,-20],
                   [-10,-20,-20,-20,-20,-20,-20,-10],
                   [ 20, 20,  0,  0,  0,  0, 20, 20],
                   [ 20, 30, 10,  0,  0, 10, 30, 20]])

blackKingScores = np.array([[ 20, 30, 10,  0,  0, 10, 30, 20],
                   [ 20, 20,  0,  0,  0,  0, 20, 20],
                   [-10,-20,-20,-20,-20,-20,-20,-10],
                   [-20,-30,-30,-40,-40,-30,-30,-20],
                   [-30,-40,-40,-50,-50,-40,-40,-30],
                   [-30,-40,-40,-50,-50,-40,-40,-30],
                   [-30,-40,-40,-50,-50,-40,-40,-30],
                   [-30,-40,-40,-50,-50,-40,-40,-30]])

piecePositionScores = {'wN': whiteKnightScores, 'wQ': whiteQueenScores, 'wB': whiteBishopScores,
                       'wR': whiteRookScores, 'wp': whitePawnScores, 'wK': whiteKingScores,
                       'bN': blackKnightScores, 'bQ': blackQueenScores, 'bB': blackBishopScores,
                       'bR': blackRookScores, 'bp': blackPawnScores, 'bK': blackKingScores}


def findRandomMove(validMoves):
    return random.choice(validMoves)

def findNoRecursionBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = checkmate
    bestPlayerMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = checkmate
        elif gs.stalemate:
            score = stalemate
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if score > maxScore:
            maxScore = score
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


# helper method to make first recursive call
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findBestMove(gs, validMoves, returnQueue, DEPTH):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkmate, checkmate, 1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -checkmate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


# def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
#     global nextMove
#     if depth == 0:
#         return turnMultiplier * scoreBoard(gs, validMoves)
#
#     # move ordering - implement later
#     maxScore = -checkmate
#     for move in validMoves:
#         gs.makeMove(move)
#         nextMoves = gs.getValidMoves()
#         score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
#         if score > maxScore:
#             maxScore = score
#             if depth == DEPTH:
#                 nextMove = move
#         gs.undoMove()
#         if maxScore > alpha:  # pruning
#             alpha = maxScore
#         if alpha >= beta:
#             break
#     return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    # end = time.time() + MAXDURATION
    # while time.time() < end:
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs, validMoves)

    # move ordering - implement later
    maxScore = -checkmate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

# def scoreBoard(gs):
#     if gs.checkmate:
#         if gs.whiteToMove:
#             return -checkmate
#         else:
#             return checkmate
#     elif gs.stalemate:
#         return stalemate
#
#     score = 0
#     for r in range(len(gs.board)):
#         for c in range(len(gs.board[r])):
#             square = gs.board[r][c]
#             if square != '--':
#                 piecePositionScore = 0
#                 if square[1] != 'K':
#                     if square[1] == 'p':
#                         piecePositionScore = piecePositionScores[square][r][c]
#                     else:
#                         piecePositionScore = piecePositionScores[square[1]][r][c]
#                 if square[0] == 'w':
#                     score += pieceScore[square[1]] + piecePositionScore * 0.06
#                 elif square[0] == 'b':
#                     score -= pieceScore[square[1]] + piecePositionScore * 0.06
#     if gs.inCheck:
#         score += 0.1
#     score += 0.05 * len(gs.pins)
#     score += 0.1 * len(gs.checks)
#
#     return score

def scoreBoard(gs, validMoves):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkmate
        else:
            return checkmate
    elif gs.stalemate:
        return stalemate

    score = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            square = gs.board[r][c]
            if square != '--':
                piecePositionScore = piecePositionScores[square][r][c]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore
    score += len(validMoves)*0.1
    return score


# Score board based on material
def scoreMaterial(gs):
    board = gs.board
    score = 0
    for r in board:
        for square in r:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score

def totalMaterial(gs):
    pieceScorenorm = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
    board = gs.board
    score = 0
    for r in board:
        for square in r:
            if square != '--':
                score += pieceScorenorm[square[1]]
    print(score)
    return score
















