import tkinter as tk
import random
import copy

class OthelloGame:
    def __init__(self, root, difficulty, gameMode):
        self.root = root
        self.root.title("Othello")
        self.canvas = tk.Canvas(root, width=400, height=400, bg='dark blue')
        self.canvas.pack()
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.currentPlayer = 'B'
        self.players = {'B': 'Black', 'W': 'White'}
        self.availableMoves = self.getAvailableMoves()
        self.drawBoard()
        self.createScoreLabels()
        self.updateScores()
        self.difficulty = difficulty
        self.gameMode = gameMode

    def drawBoard(self):
        self.canvas.delete('all')
        for i in range(8):
            for j in range(8):
                x0, y0 = j * 50, i *50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='BLUE')
                if self.board[i][j] != ' ':
                    color = 'black' if self.board[i][j] == 'B' else 'white'
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=color)

        for move in self.availableMoves:
            row, col = move
            x0, y0 = col * 50, row * 50
            x1, y1 = x0 + 50, y0 + 50
            self.canvas.create_oval(x0 + 20, y0 + 20, x1 - 20, y1 - 20, fill='green', outline='black')

    def getAvailableMoves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ' ':
                    if self.isValidMove(i, j):
                        moves.append((i, j))
        return moves
    
    def isValidMove(self, row, col):
        if self.board[row][col] != ' ':
            return False
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            if self.isFlippable(row, col, dr, dc):
                return True
        return False
    
    def isFlippable(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        if not (0 <= r < 8 and 0 <= c <8):
            return False
        if self.board[r][c] == self.currentPlayer:
            return False
        while (0 <= r < 8 and 0 <= c <8):
            if self.board[r][c] == ' ':
                return False
            if self.board[r][c] == self.currentPlayer:
                return True
            r, c = r + dr, c + dc
        return False
    def flipDisks(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        while self.board[r][c] != self.currentPlayer:
            self.board[r][c] = self.currentPlayer
            r, c = r + dr, c + dc
            
    def createScoreLabels(self):
        self.black_scoreLabel = tk.Label(self.root, text='Black: 0', fg='black')
        self.white_scoreLabel = tk.Label(self.root, text='White: 0', fg='black')
        self.black_scoreLabel.pack()
        self.white_scoreLabel.pack()

    def updateScores(self):
        count = self.countDisks()
        self.black_scoreLabel.config(text=f'Black: {count["B"]}')
        self.white_scoreLabel.config(text=f'White: {count["W"]}')


    def countDisks(self):
        count = {'B': 0, 'W': 0}
        for row in self.board:
            for disk in row:
                if disk in {'B', 'W'}:
                    count[disk] += 1
        return count
    
    def displayWinner(self):
        count = self.countDisks()
        if count['B'] > count ['W']:
            winner_text = "Black Wins!"
        elif count['B'] < count ['W']:
            winner_text = "White Wins!"
        else :
            winner_text = "Draw!"
        winner_label = tk.Label(self.root, text=winner_text)
        winner_label.pack()
    
    def evaluateState(self):
        count = self.countDisks()
        return count['B'] - count['W']
    
    def makeMove(self, row, col):
        if not self.isValidMove(row, col):
            return False
        self.board[row][col] = self.currentPlayer
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            if self.isFlippable(row, col, dr, dc):
                self.flipDisks(row, col, dr, dc)
        self.currentPlayer = 'W' if self.currentPlayer == 'B' else 'B'
        self.availableMoves = self.getAvailableMoves()
        self.drawBoard()
        self.updateScores()

        if not self.availableMoves:
            self.displayWinner()
        elif self.gameMode == 'Computer' and self.currentPlayer == 'W':
            self.makeComputerMove()
        return True
    

    def onClick(self, event):
        if self.gameMode == '1v1':
            if self.currentPlayer == 'B':
                col = event.x // 50
                row = event.y // 50
                if not (0 <= row < 8 and 0 <= col < 8):
                    return
                if not self.makeMove(row, col):
                    return
            elif self.currentPlayer == 'W':
                self.makeComputerMove()
        else:
            col = event.x // 50
            row = event.y // 50
            if not (0 <= row < 8 and 0 <= col < 8):
                    return
            if not self.makeMove(row, col):
                return
    
    def makeComputerMove(self):
        if self.difficulty == 'Easy':
            move, _ = self.alpha_beta(1, float('-inf'), float('inf'), True)
            self.makeMove(move[0], move[1])
        elif self.difficulty == 'Medium':
            move, _ = self.alpha_beta(3, float('-inf'), float('inf'), True)
            self.makeMove(move[0], move[1])
        elif self.difficulty == 'Hard':
            move = self.alpha_beta(5, float('-inf'), float('inf'), True)[0]
            self.makeMove(move[0], move[1])
    

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or not self.availableMoves:
            return None, self.evaluateState()
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            saved_state = copy.deepcopy(self.board)

            for move in self.availableMoves:
                temp_board = copy.deepcopy(self.board)
                self.board[move[0]][move[1]] = self.currentPlayer
                _, eval = self.alpha_beta(depth - 1, alpha, beta, False)
                self.board = copy.deepcopy(temp_board)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            saved_state = copy.deepcopy(self.board)

            for move in self.availableMoves:
                temp_board = copy.deepcopy(self.board)
                self.board[move[0]][move[1]] = self.currentPlayer
                _, eval = self.alpha_beta(depth - 1, alpha, beta, True)
                self.board = copy.deepcopy(temp_board)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval
        
def startGame(difficulty, gameMode):
    root = tk.Tk()
    game = OthelloGame(root, difficulty, gameMode)
    game.root.title(f"{game.players[game.currentPlayer]}'s turn")
    game.canvas.bind('<Button-1>', game.onClick)
    root.mainloop()

def main():
    root = tk.Tk()
    root.title("Othello Menu")

    def startEasy():
        startGame('Easy', mode.get())

    def startMedium():
        startGame('Medium', mode.get())
    
    def startHard():
        startGame('Hard', mode.get())
    mode = tk.StringVar()
    mode.set('1v1')

    difficulty_label = tk.Label(root, text="select difficulty:")
    difficulty_label.pack()

    easy_button = tk.Button(root, text="Easy", command=startEasy)
    easy_button.pack()

    medium_button = tk.Button(root, text="Medium", command=startMedium)
    medium_button.pack()

    hard_button = tk.Button(root, text="Hard", command=startHard)
    hard_button.pack()

    player_vs_player = tk.Radiobutton(root, text="1v1", variable=mode, value='1v1')
    player_vs_player.pack()

    player_vs_computer = tk.Radiobutton(root, text="Computer", variable=mode, value='Computer')
    player_vs_computer.pack()

    root.mainloop()

if __name__ == "__main__":
    main()