import sys
from itertools import combinations

INFINITY = 99999999

number_taken = [0, 0, 0, 0, 0, 0, 0, 0, 0]
rest_num = []
move = []
move1 = []
move2 = []

# def find_sum(arr):
#     arr.sort()
#     print(arr)
#     res = []
#     dfs(arr, 14, 0, res, [])
#     return res

# def dfs(self, nums, target, index, res, path):
#     if target < 0:
#         return
#     elif target == 0:
#         if len(path) == 3:
#             res.append(path)
#         return
#     for i in range(index, len(nums)):
#         if i > index and nums[i] == nums[i - 1]:
#             continue
#         self.dfs(nums, target - nums[i], i + 1, res, path + [nums[i]])

def wins(move):
    comb = combinations(move, 3)
    sum = 0
    # one of the players wins
    for i in list(comb):
        for j in i:
            sum += j
        if sum == 14:
            return True
    return False

def draw(moves):
    # draw game
    totalSum = 0
    for i in moves:
        totalSum += i
    if totalSum == 36:
        return True
    return False

def finished(hand1, hand2, moves):
    if wins(hand1) or wins(hand2) or draw(moves):
        return True
    return False

def getScore(player, oppo):
    if wins(player):
        return 100
    elif wins(oppo):
        return -100
    return 0


# ab negamax algorithm
def abnegamax(board, maxDepth, currentDepth, alpha, beta):
    if board.finished() or (maxDepth == currentDepth):
        score = board.getScore() - currentDepth
        return score, None

    bestMove = []
    bestScore = -INFINITY

    legal_moves = board.get_legal_moves()
    for newMove in legal_moves:
        newBoard = board.take_move(newMove)
        recursedScore = 0
        currentScore = 0
        currentMove = None

        # calculate the bestscore for the newstate and store
        if board.isMover() == newBoard.isMover():
            (recursedScore, currentMove) = abnegamax(newBoard, maxDepth, currentDepth + 1, max(alpha, bestScore), beta)
            currentScore = recursedScore
        else:
            (recursedScore, currentMove) = abnegamax(newBoard, maxDepth, currentDepth + 1, -beta,
                                                     -max(alpha, bestScore))
            currentScore = -recursedScore

        # Update the best score
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = []
            bestMove.append(move)

        # If we're outside the bounds, then prune: exit immediately
        if bestScore >= beta:
            return bestScore, bestMove

        # store all the moves with the same score
        if currentScore == bestScore:
            bestMove.append(move)

    return bestScore, bestMove

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get input
    arr = input().split()
    n = int(arr[0])

    # initialize moves already made
    for i in range(n):
        move.append(int(arr[i + 1]))
        number_taken[move[i]] = 1
        if i % 2 == 0:
            move1.append(int(arr[i + 1]))
        else:
            move2.append(int(arr[i + 1]))

    # initialize available moves
    for i in range(9):
        if (number_taken[i] == 0):
            rest_num.append(i)

    # add the best choice into move list
    # my_move = -1
    # if (my_move >= 0):
    #     move.append(my_move)
    #     n = n + 1

    # output the result
    # output = str(n)
    # for i in range(n):
    #     output = output + " " + str(move[i])
    # print(output)

    #test
    result = finished(move1, move2, move)
    print(move1)
    print(move2)
    print(result)

