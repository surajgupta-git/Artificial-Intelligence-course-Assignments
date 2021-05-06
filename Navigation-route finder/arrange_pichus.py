#!/usr/local/bin/python3
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
# Submitted by : [Suraj Gupta Gudla and surgudla]
# Based on skeleton code in CSCI B551, Spring 2021
#
import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' ]

#check if the pichu added is valid or not through checking/validating all points in its row and column
#if a pichu 'P' is added, it is a valid move if it firstly has either '@' or 'X' in its row/column as its neighbour rather than another 'P' as its neighbour
def isPValid(board,r,c):
    for i in range(r+1,len(board)):
        if board[i][c]=='X' or board[i][c]=='@': break
        if board[i][c]=='p': return False
    for i in range(r-1,-1,-1):
        if board[i][c]=='X' or board[i][c]=='@': break
        if board[i][c]=='p': return False
    for i in range(c+1,len(board[0])):
        if board[r][i]=='X' or board[r][i]=='@': break
        if board[r][i]=='p': return False
    for i in range(c-1,-1,-1):
        if board[r][i]=='X' or board[r][i]=='@': break
        if board[r][i]=='p': return False
    return True

# check if board is a goal state
def is_goal(board, k):
    if count_pichus(board)==k:
        for row in range(0,len(board)):
            for col in range(0,len(board[0])):
                if(board[row][col]=='p'):
                    if isPValid(board,row,col)==False:
                        return False
        return True
    else:
        return False

def goodforgoal(board):
    for row in range(0,len(board)):
        for col in range(0,len(board[0])):
            if(board[row][col]=='p'):
                if isPValid(board,row,col)==False:
                    return False
    return True

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_board, k):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors( fringe.pop() ):
            if count_pichus(s)>k: break
            if is_goal(s, k): return(s,True)
            if goodforgoal(s): fringe.append(s)
    return ([],False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is K, the number of agents
    k = int(sys.argv[2])
    #k=7
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    (newboard, success) = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_board(newboard) if success else "None")
