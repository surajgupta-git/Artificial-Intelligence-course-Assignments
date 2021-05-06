## Assignment 0 Report - Suraj Gupta Gudla (surgudla)

# Part 1: Navigation

## Search Abstraction
1. Initial state: 'P' - location of pichu
2. Goal state: '@'
3. State space: 'P', 'X', '.', '@'
4. successor function: either '.' or 'X'
5. cost function: uniform

## How my solution works !!
Initially we find out the pichu location on the board which is the intial state.
This inital state of pichu is added to the fringe. (the fringe is declared in such a way that it contains a combination of row and column co-ordinates, distance/count steps travelled so far, and the direction/step taken to reach that point )
I have modified the "moves" function that calculates all the next possible moves by including an additional parameter which is the step direction either U, D, L or R. Now this direction is linked to the location (row, column) and now i am easily able to track the directions and concatinating them to form a string if it finds a optimal path.
The given code had the fringe popped in a LIFO manner i.e. a stack data structure, I have modified the code such that the states from the fringe are popped in a FIFO order i.e. a queue data structure so that we follow a Breadth First Search algorithm

```(curr_move,path_str,steps_count)=fringe.pop(0)```

we iterate/repeat the logic over the fringe till it is left with no next possible moves or till it has reached the goal state.
* when we find the goal state, we return the path string and step count.
* or else we keep adding the newly visited states to the fringe (already visited states are ignored)
* if we are not able to reach the goal after traversing all possible paths, we return -1 and null path.

## Prolems faced:
Initially the code which i wrote goes to an infinite loop when it is not able find a goal state.
So I thought of discarding the already visited states by creating a list called "visited_states" to keep track of the visited states.
```visited_states.append(curr_move)```

so while appending the states to the fringe, it only adds those states are are not previously visited while finding a path to the target.
by doing this, loop terminates finitely as it has traversed all possible paths in the case when it is not able to find the goal or goal(@) does does not exist scenarios.

## Simplifications/ Design modifications
1. I have modified the "moves" function that calculates all the next possible moves by including an additional parameter which is the step direction either U, D, L or R.
Now this direction is indirectly linked to the location ( row, column) and now i am easily able to track the directions and adding them to a string if it finds a optimal path.
2. I have modified the code such that the states from the fringe are popped in a FIFO order i.e. a queue data structure so that we follow a Breadth First Search algorithm

## Other approaches tried
I also tried of linking the step direction to the location tuple(row, column) by using a dictionary( key and value pair) instead of a list but couldn't make it as the code was getting complex and got a lot of syntactical errors as i have no prior hand-on python and i am getting better day by day.

## Why does the program often fail to and a solution? Implement a fix to make the code work better.
The initial code fails as the fringe is a stack data structure and it goes to an infinite loop and pops states a LIFO order which leads to infinite loop by travewrsing the revisited states again and again .
I have modified such that the states from the fringe are popped in a FIFO order i.e. a queue data structure so that we follow a Breadth First Search algorithm. [(curr_move,path_str,steps_count)=fringe.pop(0)]
I have also created a list to keep track of the visited states to avoid the infinite loop condition.

# Part 2: Hide and Seek 

## Search Abstraction
1. Initial state: Board with an agent 'P' already placed
2. Goal state: arrangement of all K number of agents on the board such that no two agents see each other
4. state space: any arrangement of 1 to k agents on the board
3. set of valid states: any arrangement of 1 to k agents on the board such that no two agents see each other.
4. successor function: Place an agent 'P' on any '.' present on the board 
5. cost function: uniform or irrelevant

## How my solution works !!
Initally we have the board with an agent 'P' already placed and this state of the board is added to the fringe which is declared as a stack data structure here.
The states are then popped from the fringe in a LIFO manner which implies a DFS algorithm.
Then we find the successor states of the state popped.
We iterate/ repeat the the logic over the states in fringe and compare the successor states to the goal state to
* return the answer if we find the goal state
* or else append the state to the fringe
* If the fringe become empty, then we are not able arrange k agents and we return "None".
I have also created the "isPValid()" function such that after adding an agent 'P' it checks if the board state is valid or not by 
checking if the added agent has either 'X' or '@' as its neighbour(acts as an obstructor) on either of its either of its sides(all directions - up, down, right & left) on its row and column which helps in placing another 'P' on its row or column in the future moves.
  
## Simplifications/ design modifications:
The initial code takes a lot of time to run to find the goal state when the 'K' value is higher.
I have reduced the running time by adding only those valid states to the fringe that bring the board closer to goal state by creating a function "goodforgoal()".
Here "goodforgoal()" function acts as an heuristic and helps us in choosing only the good states.

          ```def goodforgoal(board):
              for row in range(0,len(board)):
                  for col in range(0,len(board[0])):
                      if(board[row][col]=='p'):
                          if isPValid(board,row,col)==False:
                              return False
              return True
              if goodforgoal(s): fringe.append(s)```
    
    
I have also created the "isPValid()" function such that after adding an agent 'P' it checks if the board state is valid or not by 
checking if the added agent has either 'X' or '@' as its neighbour(acts as an obstructor) on either of its either of its sides(all directions - up, down, right & left) on its row and column which helps in placing another 'P' on its row or column in the future moves.



































