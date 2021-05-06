#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: sgaraga-sgudla-bgoginen
#
# Based on skeleton code by D. Crandall, January 2021
#

import sys
import collections
import copy
import numpy as np
import heapq

numRows = 4
numCols = 5

# prints the board
def printable_board(board):
    return [('%3d ') * numCols % board[j:(j + numCols)] for j in range(0, numRows * numCols, numCols)]

# return a list of possible 9 successors
def successors(board_state):


    next_succ = []
    Left1 = np.roll(board_state[0:5],-1)  #using numpy as np rotating the row to the left
    Left1 = list(Left1)
    for i in range(5, 20):
        Left1.append(board_state[i])
    next_succ.append((Left1, "L1"))

    Up1 = copy.deepcopy(board_state)
    Up1_1 = np.roll(board_state[0:16:5], -1)   #using numpy as np rolling the 1st column up
    j = 0
    for i in range(0, 16, 5):
        Up1[i] = Up1_1[j]
        j += 1
    next_succ.append((Up1, "U1"))

    Right2 = []
    Right2_1 = np.roll(board_state[5:10], 1)    #using numpy as np rolling the 2nd row right
    for i in range(0, 5):
        Right2.append(board_state[i])
    for i in range(0, 5):
        Right2.append(Right2_1[i])
    for i in range(10, 20):
        Right2.append(board_state[i])
    next_succ.append((Right2, "R2"))

    Down2 = copy.deepcopy(board_state)
    Down2_1 = np.roll(board_state[1:17:5], 1)     #using numpy as np rolling the 2nd column down
    j = 0
    for i in range(1, 17, 5):
        Down2[i] = Down2_1[j]
        j += 1
    next_succ.append((Down2, "D2"))

    Left3 = []
    Left3_1= np.roll(board_state[10:15],-1)       #using numpy as np rolling the 3rd row left
    for i in range(0, 10):
        Left3.append(board_state[i])
    for i in range(0, 5):
        Left3.append(Left3_1[i])
    for i in range(15, 20):
        Left3.append(board_state[i])
    next_succ.append((Left3, "L3"))


    Up3 = copy.deepcopy(board_state)
    Up3_1 = np.roll(board_state[2:18:5], -1)      #using numpy as np rolling the 3rd column up
    j = 0
    for i in range(2, 18, 5):
        Up3[i] = Up3_1[j]
        j += 1
    next_succ.append((Up3, "U3"))

    Right4 = []
    Right4_1 = np.roll(board_state[15:20], 1)     #using numpy as np rolling the 4th row right
    for i in range(0, 15):
        Right4.append(board_state[i])
    for i in range(0, 5):
        Right4.append(Right4_1[i])
    next_succ.append((Right4, "R4"))


    Down4 = copy.deepcopy(board_state)
    Down4_1 = np.roll(board_state[3:19:5],1)       #using numpy as np rolling the 4th column down
    j = 0
    for i in range(3, 19, 5):
        Down4[i] = Down4_1[j]
        j += 1
    next_succ.append((Down4, "D4"))

    Up5 = copy.deepcopy(board_state)
    Up5_1 = np.roll(board_state[4:20:5], -1)       #using numpy as np rolling the 5th column up
    j = 0
    for i in range(4, 20, 5):
        Up5[i] = Up5_1[j]
        j += 1
    next_succ.append((Up5, "U5"))

    return next_succ

# check if we have reached the goal state or not
def is_goal(state):
    for i in range(0, 20):
        if state[i] == i + 1:
            continue
        else:
            return False
    return True

#heurisitc function to find the misplaced number of tiles for each board state
def num_of_misplaced_tiles(boardState):
    boardState = tuple(boardState)
    Count = 0
    for i in range(0, 20):
        if boardState[i] != i + 1:
            Count = Count + 1
    return Count


def solve(initial_boardState):
    initial_boardState = list(initial_boardState)
    fringe = []
    heapq.heappush(fringe, (0, initial_boardState, [], 0))
    while fringe:
        fringeElement = heapq.heappop(fringe)     # pops the list with less priority.
        priority = fringeElement[0]
        parentState = fringeElement[1]
        pathToParent = fringeElement[2]
        nextmoveCost = fringeElement[3]
        nextmoveCost = nextmoveCost + 1
        if is_goal(parentState):
            return pathToParent
        for x in successors(parentState):
            path_parent_temp = copy.deepcopy(pathToParent)
            childState = x[0]
            Direction_child = x[1]         #to store the direction of the movement.
            path_parent_temp.append(Direction_child)
            if is_goal(childState):
                return path_parent_temp
            total = num_of_misplaced_tiles(childState) + nextmoveCost
            heapq.heappush(fringe, (total, childState, path_parent_temp, nextmoveCost))   # pushing all the successors for a given state of the board.
    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if (len(sys.argv) != 2):
       raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != numRows * numCols:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
