"""
Main drive file for handling user input and displaying current GameState object
"""

import pygame as p
from Chess import ChessEngine, ChessAI
from multiprocessing import Process, Queue

p.init()
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', "bp", "bR", "bN", "bB", 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("imagesc/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # access image with 'IMAGES['wp']


def main():
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    moveLogFont = p.font.SysFont('Arial', 15, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when move is made. this way we only have to generate valid moves once per move
    animate = False  # flag variable for when to animate move
    loadImages()
    running = True
    sqSelected = ()  # tracks last click of user
    playerClicks = []  # tracks player clicks (two tuples)
    gameOver= False
    playerOne = False  # True if human is white, false if AI is white
    playerTwo = True  # same for black
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:  # can delete this human turn when you fix bug where if you click on ai piece while AI think you cant move during ur turn
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:  # user clicks same square twice
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append 1st and second clicks
                    if len(playerClicks) == 2 and humanTurn:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        #AI move finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                returnQueue = Queue()
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gs, validMoves, returnQueue, ChessAI.DEPTH))
                moveFinderProcess.start()  # call findBestMove(gs, validMoves, return Queue)

            if not moveFinderProcess.is_alive():
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = ChessAI.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        drawGameState(screen, gs, validMoves, sqSelected, gs.moveLog, moveLogFont)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, 'Black wins by checkmate')
            else:
                drawEndGameText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawEndGameText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs, validMoves, sqSelected, moveLog, moveLogFont):
    drawBoard(screen)
    # add in move suggestions later
    highlightSquares(screen, gs, validMoves, sqSelected, moveLog)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    drawScore(screen, gs, validMoves)

def highlightSquares(screen, gs, validMoves, sqSelected, moveLog):  # pass move log in to add highlighting last move
    if moveLog:  # highlights last move made
        lastMove = moveLog[-1]
        sr, sc = lastMove.startRow, lastMove.startCol
        er, ec = lastMove.endRow, lastMove.endCol
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(200)  # transparency value 0 - 255 (opaque)
        s.fill(p.Color('dimgray'))
        screen.blit(s, (sc * SQ_SIZE, sr * SQ_SIZE))
        screen.blit(s, (ec * SQ_SIZE, er * SQ_SIZE))


    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # square selected is piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value 0 - 255 (opaque)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight all moves from that square
            s.set_alpha(150)
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    s.set_alpha(100) if (move.endCol+move.endRow)%2 == 0 else s.set_alpha(150)
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawBoard(screen):  # future add letter/num for notation to board
    global colors
    colors = [p.Color('light grey'), p.Color('dark green')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + '. ' + str(moveLog[i]) + ' '
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)

    movePerRow = 3
    padding = 5
    textY = padding
    lineSpacing = 2
    for i in range(0, len(moveTexts), movePerRow):
        text = ''
        for j in range(movePerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j] + '  '
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move one square. edit to make longer move be shorter ie all animations same length
    frameCount = min(((abs(dR) + abs(dC)) * framesPerSquare), 45)  # make it so animation takes 3/4 of a second max
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase piece move from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    font = p.font.SysFont('Helvitca', 50, True, False)
    textObject = font.render(text, 0, p.Color('white'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('black'))
    screen.blit(textObject, textLocation.move(1, 1))

def drawScore(screen, gs, validMoves):
    font = p.font.SysFont('Arial', 50, True, False)
    score = str(ChessAI.scoreMaterial(gs) // 100)  # scoreMAterial for material score. scoreBoard for evalbar
    scoreObject = font.render(score, 0, p.Color('white'))
    scoreLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH + 10, BOARD_HEIGHT - 60)
    screen.blit(scoreObject, scoreLocation)

    eval = str(round(ChessAI.scoreBoard(gs, validMoves)/100, 2))[0:6]  # scoreMAterial for material score. scoreBoard for evalbar
    evalObject = font.render(eval, 0, p.Color('white'))
    evalLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH + 130, BOARD_HEIGHT - 60)
    screen.blit(evalObject, evalLocation)

if __name__ == '__main__':
    main()




















