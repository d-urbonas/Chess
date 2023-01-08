import random
import numpy as np

pieceScore = {'K': 20000, 'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'p': 100}
checkmate = 100000
stalemate = 0
DEPTH = 3
QUIESCENCEDEPTH = 1

''' future improvments: 
1. Transposition table (needs zobrist hashing), 
2. Iterative deepening - evaluate each depth of minmax until time limit is reached. use previous results to improve move ordering 
3. Pawn position eval. ex. chains good stacked bad
4. improve quiescence search. idea - only look at the following captures of the determined best move and if it turns,
        that move is a mistake then look at the best next move. (not sure if this is possible with how pruning works)

'''
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
                   [ 5, -5,-10,-20,-20,-10, -5,  5],
                   [ 5, 10, 10,-40,-40, 10, 10,  5],
                   [ 0,  0,  0,  0,  0,  0,  0,  0]])

blackPawnScores = np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
                   [ 5, 10, 10,-40,-40, 10, 10,  5],
                   [ 5, -5,-10,-20,-20,-10, -5,  5],
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

def findBestMove(gs, validMoves, returnQueue, DEPTH):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    for move in validMoves:  # moves all pawn to moves to back to be checked last. improves pruning
        if move.pieceMoved[1] == 'p':
            validMoves.remove(move)
            validMoves.append(move)
    # increase depth when only a couple now pawns left ie so can find mates better.
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkmate, checkmate, 1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return quiescence(alpha, beta, gs, validMoves, turnMultiplier, QUIESCENCEDEPTH)

    # move ordering - implement later
    maxScore = -checkmate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        for j in nextMoves:
            if j.pieceMoved[1] == 'p':
                nextMoves.remove(j)
                nextMoves.append(j)
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

def quiescence(alpha, beta, gs, validMoves, turnMultiplier, depth):  # keeps evaluationg continous captures beyond the specified depth to avoid obvious blunders
    if depth == 0:
        return turnMultiplier * scoreBoard(gs, validMoves)
    stand_pat = turnMultiplier * scoreBoard(gs, validMoves)
    if stand_pat >= beta:
        return beta
    alpha = max(alpha, stand_pat)

    for move in validMoves:
        if move.isCapture:
            gs.makeMove(move)
            score = -quiescence(-beta, -alpha, gs, gs.getValidMoves(), -turnMultiplier, QUIESCENCEDEPTH - 1)
            gs.undoMove()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

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
    if len(gs.moveLog) > 8:
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
    pieceScoreMaterial = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
    board = gs.board
    score = 0
    for r in board:
        for square in r:
            if square != '--':
                score += pieceScoreMaterial[square[1]]
    print(score)
    return score
