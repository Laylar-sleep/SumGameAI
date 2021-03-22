import time
from itertools import combinations

INFINITY = 99999999

class Board:
    def __init__(self, arr):
        self.number_taken = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rest_num = []
        self.move = []
        self.move1 = []
        self.move2 = []
        self.n = 0
        self.mover = 0
        # initialize moves already made
        self.n = int(arr[0])
        for i in range(self.n):
            self.move.append(int(arr[i + 1]))
            self.number_taken[self.move[i]] = 1
            if i % 2 == 0:
                self.move1.append(int(arr[i + 1]))
            else:
                self.move2.append(int(arr[i + 1]))

        # initialize available moves
        for i in range(9):
            if (self.number_taken[i] == 0):
                self.rest_num.append(i)

        # set mover
        if self.n % 2 == 0:
            self.mover = 1 # player two
        else:
            self.mover = 0 # player one

    def getHand(self, player):
        if player == 0:
            hand = self.move1
        else:
            hand = self.move2
        return hand

    def getSum(self, hand):
        comb = combinations(hand, 3)
        sum = []
        for i in list(comb):
            tmp = 0
            for j in i:
                tmp += j
            sum.append(tmp)

        return sum


    def wins(self, player):
        # print("  check win " + str(player))
        hand = []
        hand = self.getHand(player)

        if len(hand) < 3:
            return False
        sum = self.getSum(hand)
        for i in sum:
            if i == 14:
                return True
        return False

    def draw(self, moves):
        # draw game
        if len(moves) == 9:
            return True
        else:
            return False

    def finished(self):
        if self.wins(self.mover) or self.wins(not self.mover) or self.draw(self.move):
            return True
        return False

    def getScore(self, depth):

        if self.wins(self.mover):
            # print("  "+str(self.mover) + " mover wins " + str(-100+depth))
            return -100 + depth
        return 50-depth

    def take_move(self, newMove):
        # update new game board
        arr = []
        newCount = self.n + 1
        arr.append(newCount)
        arr = arr + self.move
        arr.append(newMove)
        newBoard = Board(arr)

        # test
        # print("moves: " + str(newBoard.move))
        # print("available moves: " + str(newBoard.rest_num))

        return newBoard

# ab negamax algorithm
def abnegamax(board, maxDepth, currentDepth, alpha, beta):
    # check if resursing is done
    if board.finished() or (maxDepth == currentDepth):
        finalScore = board.getScore(currentDepth)
        return finalScore, None

    bestMove = None
    bestScore = -INFINITY

    # go through each move
    legal_moves = board.rest_num

    for newMove in legal_moves:
        newBoard = board.take_move(newMove)
        recursedScore = 0
        currentScore = 0
        currentMove = None

        # Recurse
        recursedScore, currentMove = abnegamax(newBoard, maxDepth, currentDepth + 1, -beta,
                                                     -max(alpha, bestScore))
        currentScore = -recursedScore

        # Update the best score
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = newMove

        # If we're outside the bounds, then prune: exit immediately
        if bestScore >= beta:
            return bestScore, bestMove

    return bestScore, bestMove

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get input
    arr = input().split()
    time_start = time.time()
    board = Board(arr)

    # add the best choice into move list
    my_score, my_move = abnegamax(board, 9, 0, -INFINITY, INFINITY)
    if (my_move >= 0):
        board.move.append(my_move)
        board.n = board.n + 1

    # output the result
    output = str(board.n)
    for i in range(board.n):
        output = output + " " + str(board.move[i])
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    print(output)

