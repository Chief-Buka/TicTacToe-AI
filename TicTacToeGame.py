import math

class TicTacToe():
    def __init__(self):
        self.X = "X"
        self.O = "O"
        self.EMPTY = None
        self.bestMoves = {}


    def initialState(self):
        """
        Returns starting state of the board.
        """
        board = []
        for row in range(self.size):
            board.append([])
            for col in range(self.size):
                board[row].append(self.EMPTY)
        return board

    #which players turn
    def player(self, board):
        countX = 0
        countO = 0
        for row in board:
            for spot in row:
                if (spot == self.X):
                    countX += 1
                elif (spot == self.O):
                    countO +=1
        if (countX == countO):
            return self.X
        else:
            return self.O


    #available actions
    def actions(self, board):
        emptySpaces = set()
        for i in range(self.size):
            for j in range(self.size):
                if (board[i][j] == self.EMPTY):
                    emptySpaces.add((i,j))
        return emptySpaces

    #return result of putting 
    def result(self, board, action):
        if (action[0] > (self.size-1) or action[0] < 0 or
            action[1] > (self.size-1) or action[1] < 0 or
            board[action[0]][action[1]] != self.EMPTY):
            raise ValueError
        else:
            temp = self.initialState()
            for i in range(self.size):
                for j in range(self.size):
                    temp[i][j] = board[i][j]
            temp[action[0]][action[1]] = self.player(board)
            return temp


    def winner(self, board):
        if ( self.horizontalWin(board, self.X) or self.verticalWin(board, self.X) or self.diagWin(board, self.X)):
            return self.X
        elif ( self.horizontalWin(board, self.O) or self.verticalWin(board, self.O) or self.diagWin(board, self.O)):
            return self.O
        else:
            return None

    def horizontalWin(self, board, player):
        for row in board:
            count = 0
            for space in row:
                if (space == player):
                    count+=1
            if (count == self.size):
                return True
        return False

    def verticalWin(self, board, player):
        for j in range(self.size):
            count = 0
            for i in range(self.size):
                if (board[i][j] == player):
                    count+=1
            if (count == self.size):
                return True
        return False

    def diagWin(self, board, player):
        countTLBR= 0
        countTRBL = 0
        for i in range(self.size):
            for j in range(self.size):
                if ((i == j) and (board[i][j] == player)):
                    countTLBR += 1
                if ((i+j == self.size-1) and (board[i][j] == player)):
                    countTRBL +=1
        if (countTLBR == self.size or countTRBL == self.size):
            return True
        return False

    #check
    def terminal(self, board):
        isWin = self.winner(board)
        if (isWin == self.X or isWin == self.O):
            return True
        for row in board:
            for space in row:
                if (space == self.EMPTY):
                    return False
        return True

    #check
    def utility(self, board):
        isWin = self.winner(board)
        power = len(self.actions(board))+1
        if (isWin == self.X):
            return power
        elif (isWin == self.O):
            return -power
        else:
            return 0

    def printBoard(self, board):
        print("   ", end="")
        for i in range(self.size):
            print(f" {i} |", end="")
        print()
        n = 0
        for row in board:
            print(f"{n} | ", end="")
            n+=1
            for pos in row:
                if pos == self.EMPTY:
                    print(" ", end="")
                else:
                    print(pos, end="")
                print(" | ", end="")
            print()

    def waitForMove(self, currPlayer):
        temp = input('What is your move?: ')
        move = (int(temp[0]), int(temp[2]))
        return move

    def game(self):
        self.size = int(input("What should be the size of the board?: "))
        board = self.initialState()
        while(True):
            playerMove = None
            self.printBoard(board)
            currPlayer = self.player(board)
            print(f"It is player {currPlayer}'s turn")
            if (currPlayer == self.O):
                print(f"Player {currPlayer} is thinking...")
                self.bestMoves = {}
                value = self.minimax(board, currPlayer, 0, -math.inf, math.inf)
                print(self.bestMoves)
                playerMove = self.bestMoves[value]
                board = self.result(board, playerMove)
            else:
                while(playerMove == None):
                    try:
                        playerMove = self.waitForMove(currPlayer)
                        print()
                        board = self.result(board, playerMove)
                    except ValueError:
                        print("Please enter a valid position")
        
            if (self.winner(board)):
                self.printBoard(board)
                print(f"{currPlayer} wins!!!")
                return
            if (self.terminal(board)):
                self.printBoard(board)
                print("Its a tie mate")
                return


    def minimax(self, board, currPlayer, depth, alpha, beta):
        if (self.terminal(board)):
            return self.utility(board)
        if (currPlayer == self.X):
            maxValue = -math.inf
            for action in self.actions(board):
                value = self.minimax(self.result(board, action), self.O, depth+1, alpha, beta)
                maxValue = max(value, maxValue)
                alpha = max(alpha, maxValue)
                if (beta < alpha):
                    break
            return maxValue
        else:
            minValue = math.inf
            for action in self.actions(board):
                value = self.minimax(self.result(board, action), self.X, depth+1, alpha, beta)
                minValue = min(value, minValue)
                beta = min(beta, minValue)
                if (beta < alpha):
                    break
                if (depth == 0 and minValue == value):
                    self.bestMoves[minValue] = action
            return minValue 

play = TicTacToe()
play.game()