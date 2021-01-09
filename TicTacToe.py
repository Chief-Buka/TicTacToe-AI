import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

#which players turn
def player(board):
    countX = 0
    countO = 0
    for row in board:
        for spot in row:
            if (spot == X):
                countX += 1
            elif (spot == O):
                countO +=1
    if (countX == countO):
        return X
    else:
        return O


#available actions
def actions(board):
    emptySpaces = set()
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                emptySpaces.add((i,j))
    return emptySpaces

#return result of putting 
def result(board, action):
    if (action[0] > 2 or action[0] < 0 or
        action[1] > 2 or action[1] < 0 or
        board[action[0]][action[1]] != EMPTY):
        raise ValueError
    else:
        temp = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        for i in range(3):
            for j in range(3):
                temp[i][j] = board[i][j]
        temp[action[0]][action[1]] = player(board)
        return temp


def winner(board):
    if ( horizontalWin(board, X) or verticalWin(board, X) or diagWin(board, X)):
        return X
    elif ( horizontalWin(board, O) or verticalWin(board, O) or diagWin(board, O)):
        return O
    else:
        return None

def horizontalWin(board, player):
    for row in board:
        count = 0
        for space in row:
            if (space == player):
                count+=1
        if (count == 3):
            return True
    return False

def verticalWin(board, player):
    for j in range(3):
        count = 0
        for i in range(3):
            if (board[i][j] == player):
                count+=1
        if (count == 3):
            return True
    return False

def diagWin(board, player):
    countTLBR= 0
    countTRBL = 0
    for i in range(3):
        for j in range(3):
            if ((i == j) and (board[i][j] == player)):
                countTLBR += 1
            if ((i+j == 2) and (board[i][j] == player)):
                countTRBL +=1
    if (countTLBR == 3 or countTRBL == 3):
        return True
    return False

#check
def terminal(board):
    isWin = winner(board)
    if (isWin == X or isWin == O):
        return True
    for row in board:
        for space in row:
            if (space == EMPTY):
                return False
    return True

#check
def utility(board):
    isWin = winner(board)
    power = len(actions(board)+1)
    if (isWin == X):
        return power
    elif (isWin == O):
        return -power
    else:
        return 0

def printBoard(board):
    print("    0 | 1 | 2 |")
    n = 0
    for row in board:
        print(f"{n} | ", end="")
        n+=1
        for pos in row:
            if pos == EMPTY:
                print(" ", end="")
            else:
                print(pos, end="")
            print(" | ", end="")
        print()

def waitForMove(currPlayer):
    temp = input('What is your move?: ')
    move = (int(temp[0]), int(temp[2]))
    return move

def game():
    board = initial_state()
    while(True):
        playerMove = None
        printBoard(board)
        currPlayer = player(board)
        print(f"It is player {currPlayer}'s turn")
        if(currPlayer == O):
            playerMove = minimax(board, currPlayer)
            board = result(board, playerMove)
        else:
            while(playerMove == None):
                try:
                    playerMove = waitForMove(currPlayer)
                    print()
                    board = result(board, playerMove)
                except ValueError:
                    print("Please enter a valid position")
    
        if (winner(board)):
            printBoard(board)
            print(f"{currPlayer} wins!!!")
            return


def minimax(board, currPlayer):
    if (terminal(board)):
        return utility(board)
    if (currPlayer == X):
        maxValue = -math.inf
        for action in actions(board):
            tempBoard = results(board, action)
            value = minimax(tempBoard, O)
            maxValue = max(value, maxValue)
            return maxValue
    else:
        minValue = math.inf
        for action in actions(board):
            tempBoard = results(board, action)
            value = minimax(tempBoard, X)
            minValue = min(value, maxValue)
            return minValue 

