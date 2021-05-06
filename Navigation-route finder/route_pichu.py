#
# route_pichu.py : a maze solver
# Submitted by : [Suraj Gupta Gudla - surgudla]
# Based on skeleton code provided in CSCI B551, Spring 2021.
import sys
import json

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Return a string with the board rendered in a human/pichu-readable format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col,step):
        moves=((row+1,col,step+'D'), (row-1,col,step+'U'), (row,col-1,step+'L'), (row,col+1,step+'R'))
	# Return only moves that are within the board and legal (i.e. go through open space "."), returns a list
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        # Adding the inital state to the fringe
        fringe=[(pichu_loc,'',0)]
        visited_states=[] # a list to store all visisted states
        while fringe: #repeat the logic till the fringe becomes empty
                (curr_move,path_str,steps_count)=fringe.pop(0) #popping from queue implies BFS
                visited_states.append(curr_move)
                for nextmove in moves(house_map,curr_move[0],curr_move[1],path_str): #iterating over all the next possible moves
                        if house_map[nextmove[0]][nextmove[1]]=="@":
                        # if the state is goal state return the path string and step count
                                return (steps_count+1,nextmove[2])
                        else: #else append the state to the fringe if it is not already visited
                                if (nextmove[0:2] not in visited_states):
                                        fringe.append((nextmove[0:2],nextmove[2],steps_count+1))
        return(-1,"")

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Routing in this board:\n" + printable_board(house_map) + "\n")
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + str(solution[1]))



