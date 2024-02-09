import random as rd
# importing random for easier bots
# This is a custom module that I will import in the main file
# I will use a class structure since it will be easier in the game
class TicTacToe:
    # the init function
    def __init__(self):
        # difficulty is equivalent to depth for the Minimax function
        self.difficulty = 9
        # gb is the gameboard, a dict of " "
        self.gb = dict(enumerate([" " for sq in range(9)]))
        # best_move will be used for later, to determine the best move
        self.best_move = None
        # debug isn't neccessary, but its helpful for when I write the program.
        # debug shows the number of times minimax has been called, useful for a recursive function 
        self.debug = 0
        self.top_moves = []
    # a helper function we can use later
    # sets the difficulty

    # I will use this in the main file
    # to change the difficulty
    # useful as tkinter IntVar
    def setter(self, *args):
        if args[0] < 1: self.difficulty = 1
        elif args[0] > 10: self.difficulty = 10
        else: self.difficulty = args[0]
    # resets the gameboard for the next game
    def reset(self):
        self.gb = dict(enumerate([" " for sq in range(9)]))
    # checks if a player has won, this I chose to hardcode since the rules dont change
    def checkWin(self, player):
        # O: first index (0), W: second index (1), etc etc
        O, W, T, U, V, X, S, E, N = self.gb[0],self.gb[1],self.gb[2],\
        self.gb[3],self.gb[4],self.gb[5],self.gb[6],self.gb[7],self.gb[8]
        if (O == W and O == T and O == bool(player)): return True
        elif (S == E and S == N and S == bool(player)): return True
        elif (T == X and T == N and T == bool(player)): return True
        elif (O == V and O == N and O == bool(player)): return True
        elif (W == V and W == E and W == bool(player)): return True
        elif (S == V and S == T and S == bool(player)): return True
        elif (U == V and U == X and U == bool(player)): return True
        elif (O == U and O == S and O == bool(player)): return True
        else: return False # otherwise return false
    # this is a useful function that we will use later
    # returns all the open spots on the board
    # since this is tic tac toe, these are all the legal spots
    def free_spots(self):
        # creates a new temporary list of indeces that are free
        indices = []
        for i in dict(self.gb).keys():
            if self.gb[i] == " ":
                indices.append(i)
        # returns the indeces (indexes) of the empty spots
        return indices
    # the minimax function searches all the nodes in the tree, then returns the best moves
    # this is also a DFS, a very commonly used search algortithm
    # I used a b for variables alpha and beta because it is easier to see the logic
    # and also because alpha and beta don't mean anything, they are almost like placeholders 
    def Minimax(self, is_computer: bool, a: int, b: int, depth_lim: int):
        self.debug +=+ 1
        ###############################################
        #     self.debug += 1
        #     self.debug -=- 1
        #     self.debug +=-- 1
        ###############################################
        # the code below is used for the difficulty setting
        # basically the depth setting. If the depth is at 0, then
        # we stop the search and return an evaluation of that position
        # depth basically means how many moves we look ahead
        if depth_lim == 0:
            if self.checkWin(True): return 1
            elif self.checkWin(False) and not self.checkWin(True): return -1
            else: return 0
        # this is to make sure the game is still going and no one has won yet
        # since we are the computer, X winning is good, so we return a score of 100
        # while losing returns a score of -100. Ties are 0
        if self.checkWin(True): return 100
        elif self.checkWin(False) and not self.checkWin(True): return -100
        elif len(self.free_spots()) == 0: return 0
        elif is_computer:
        # this means it is our turn in the tree of positions
            best_evaluation = -1000
            # checks the free spots, loops over them
            for square in self.free_spots():
                # temporarily set the spot to be "X"
                self.gb[square] = True
                # call the minimax funciton again, which makes this a recursive function
                node_eval = self.Minimax(not is_computer, a, b, depth_lim - 1)
                # we undo the move to retain the gameboard
                self.gb[square] = " "
                # if the move we looked at was better than the best move that we have seen
                # so far, then we update the best_evaluation
                if node_eval >= best_evaluation: best_evaluation = node_eval
                # a b pruning is a little hard to understand
                # basically, if the move we are looking at is so bad that 
                # we immediately (or can be forced to) lose, we don't waste
                # precious time and resources searching a futile position
                a = max(a, node_eval)
                if b <= a: break
            # return the best evaluation for the node we are searching
            return best_evaluation
        # otherwise, it is the players turn in the tree of positions
        else:
            # they would rather choose something that lowers the evaluation,
            # quite similar to chess, where the lower the number, the more
            # if favors black (player), and the higher the evaluation
            # the more it favors white (computer)
            # This is basically an identical copy of the code above, except inverted          
            best_evaluation = 1000
            for square in self.free_spots():
                self.gb[square] = False
                node_eval = self.Minimax(not is_computer, a, b, depth_lim - 1)
                self.gb[square] = " "
                if node_eval <= best_evaluation: best_evaluation = node_eval
                b = min(b, node_eval)
                if b <= a: break
            return best_evaluation
    # this method sprinkles some randomness into the moves of the computer if
    # the difficulty is less than a certain number (ex. 3)
    # shown in line 125
    # this is the initializing function for the minimax, we choose the move that
    # leads to the best evaluation for us
    def mmx(self):
        # basically the same thing as the minimax function for the computer side
        best_evaluation = -1000
        total_moves = []
        for square in self.free_spots():
            self.gb[square] = True
            node_eval = self.Minimax(False,-1000,1000, self.difficulty)
            self.gb[square] = " "
            if node_eval >= best_evaluation:
                best_evaluation = node_eval
                # takes the move with highest evualation, and sets it as the best move
                self.best_move = square
            total_moves.append((node_eval, square))
        total_moves = sorted(total_moves, key=lambda x: x[0], reverse=True)
        self.top_moves = [move for move in total_moves if move[0] == 100]
        # not really neccessary but cool to see the engine's evaluation
        return (best_evaluation, total_moves, self.top_moves)
            # this last piece of code is used to add in some randomness to the moves, still top moves though
    # I made this function to streamline checking if the game is a draw
    # first checks if the game is a win or lost is so, return False
    # otherwise, if there are no available space, then return True
    def checkDraw(self):
        if self.checkWin(True) or self.checkWin(False):
            return False
        # .keys() returns the keys (almost like indexes) of a dict, in this case our gameboard
        for key in self.gb.keys():
            if self.gb[key] == ' ': return False 
        return True
    # this function will play against a random bot, to test how good it is.
    def testing(self):
        x = True
        while True:
            while True:
                self.debug = 0
                self.mmx()
                print(f"{self.debug} pos searched")
                self.gb[self.best_move] = True
                try:
                    self.gb[self.free_spots()[rd.randint(0, len(list(self.free_spots())) - 1)]] = False
                except:
                    self.reset()
                    break
                print(f"Computer won:{self.checkWin(True)} Player won: {self.checkWin(False)}")
                if self.checkWin(True):
                    print("NEW GAME -------------------------------")
                    self.reset()
                elif self.checkWin(False):
                    x = False
                    break
                elif self.checkDraw():
                    self.reset()
                    print("NEW GAME -------------------------------")
            if not x: break
# good practice - testing wont run if I import it as a module
if __name__ == "__main__":
    engine = TicTacToe()
    engine.testing()