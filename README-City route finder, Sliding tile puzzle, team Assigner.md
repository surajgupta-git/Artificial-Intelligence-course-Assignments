# Assignment 1

# Part 1
### Search abstraction
*Initial State*: Any random arrangement of all the 20 tiles.
*State Space*: A state space is the set of all possible arrangements of the 20 tiles. For each state there would be 9 successors considering the right and left movement of the rows and up down movement of the columns.
Successor function: For each state there would be 9 successors considering the right and left movement of the rows and up down movement of the columns.
Cost Function: The cost function is uniform in the given problem. For each successor the cost increases by 1. F(n) = G(n) + H(n). G(n) is uniform for each stage of the successors . for the first stage of successors G(n) = 1 , for the next stage of successors it would be G(n) +G(n) = 2.
*Heuristic function*: Number of Misplaced tiles
*Admissibility of the Heuristic function*: Value of the Number of Misplaced tiles will always be less than or equal to the total cost to reach the goal as each optimal move will reduce the number of misplaced tiles by 1.
*Goal state*: All 20 tiles in their original positions
```
1   2   3    4   5
6   7   8    9   10
11  12  13   14  15
16  17  18   19  20 
```
			

### Algorithm Description:
Before starting to analyze how to reach the goal state, the first step is to choose an algorithm such that it is an informed search algorithm and is admissible. It is necessary that we estimate the cost that is lower or equal to the actual cost of reaching the goal state. h(n) <= h*(n). We used misplaced tiles as the heuristic to get the priority( (i.e) lowest number of misplaced tiles) to choose from the 9 successors for each parent state. 
In the solve function() we send the start_state as the argument. We are using a heapq which works as a priority queue to pop out the successor with less heuristic. For each state we find successors .
Suppose for the initial board	
```
1  17    3    4   5 
10   2    7    8   9 
11   6   13  14   15 
16  12   18  19    20
```
To find the successor states for a particular board we stored 9 different boards for every rotation of a single row or column and also stored the direction to keep the track of the movements followed.
We get 9 successors as:
```
([17, 3, 4, 5, 1, 10, 2, 7, 8, 9, 11, 6, 13, 14, 15, 16, 12, 18, 19, 20], 'L1')
([1, 17, 3, 4, 5, 10, 2, 7, 8, 9, 6, 13, 14, 15, 11, 16, 12, 18, 19, 20], 'L3')
([1, 17, 3, 4, 5, 9, 10, 2, 7, 8, 11, 6, 13, 14, 15, 16, 12, 18, 19, 20], 'R2')
([1, 17, 3, 4, 5, 10, 2, 7, 8, 9, 11, 6, 13, 14, 15, 20, 16, 12, 18, 19], 'R4')
([10, 17, 3, 4, 5, 11, 2, 7, 8, 9, 16, 6, 13, 14, 15, 1, 12, 18, 19, 20], 'U1')
([1, 17, 7, 4, 5, 10, 2, 13, 8, 9, 11, 6, 18, 14, 15, 16, 12, 3, 19, 20], 'U3')
([1, 17, 3, 4, 9, 10, 2, 7, 8, 15, 11, 6, 13, 14, 20, 16, 12, 18, 19, 5], 'U5')
([1, 12, 3, 4, 5, 10, 17, 7, 8, 9, 11, 2, 13, 14, 15, 16, 6, 18, 19, 20], 'D2')
([1, 17, 3, 19, 5, 10, 2, 7, 4, 9, 11, 6, 13, 8, 15, 16, 12, 18, 14, 20], 'D4')
```
Then we check if any of the board matches with the goal state,  if not then we find the cost by adding the misplaced tiles and the next move cost which is 1. We push the total, child state , path and the next move cost for every successor. 
```
while fringe:
    fringeElement = heapq.heappop(fringe)
    priority = fringeElement[0]
    parentState = fringeElement[1]
    pathToParent = fringeElement[2]
    nextmoveCost = fringeElement[3]
    nextmoveCost = nextmoveCost + 1
    if is_goal(parentState):
        return pathToParent
    for x in successors(parentState):
        print(x)
        path_parent_temp = copy.deepcopy(pathToParent)
        childState = x[0]
        Direction_child = x[1]
        path_parent_temp.append(Direction_child)
        if is_goal(childState):
            return path_parent_temp
        total = num_of_misplaced_tiles(childState) + nextmoveCost
        heapq.heappush(fringe, (total, childState, path_parent_temp, nextmoveCost))
return []
```

The above loop repeats till the fringe is empty and a goal state is reached, the fringeElement gets the correct next _successor by using the heapq.pop as it pops out the state with less total. The loop continues till the goal state is reached then the path to goal state is returned. the length of the path gives the number of moves.


*Heuristic function used*: We used the number of misplaced tiles to find the priority of the next successor to be chosen in order to receive the goal state with less cost.

*Algorithm used*: We have used A* search algorithm which is an informed search algorithm or a best first search algorithm to reach the final state from the initial state by calculating g and h at every step. g is the cost from one step to the next step and h is the heuristic value or the estimated cost of moving from one cell to the final cell. We must also make sure that there is never an over estimation of the cost.


### Difficulties:
first we were confused about which heuristic to be used such that it is admissible and it works for different boards as well.We tried different heuristics such as Manhattan distance,number of misplaced tiles and linear conflict. If one worked for a board it did not work for another so it was complicated to choose between the heuristic.

# Part 2:
### Search Abstraction:
   
*Initial state*: start city 

*State space*: All the cities present in city-gps.txt

*Successor function*: returns all the consecutive cities to a particular city

*Cost function*: The total cost can be either of the below
1. number of segments between start and end city
2. time of travel between start and end city
3. distance between start and end city
4. number of accidents in that route

*Goal state*: end city

*Heuristic function*: haversine distance between cities

   References:
   https://community.esri.com/t5/coordinate-reference-systems/distance-on-a-sphere-the-haversine-formula/ba-p/902128
   https://en.wikipedia.org/wiki/Haversine_formula
   
*Admissability of the Heuristic*:
  Since Haversine distance calculates the distance between 2 points on a sphere , it will always be less than the actual distance that will be covered in real time over a     network of highways/roads.

   
   
### Algorithm Description:
A* Search has been implemented as there are a large number of cities and it is a very big network of segments , so in order to get a solution quickly (less computational time)  we decided A* would be the best fit.

First the initial state is loaded with the start city.
A prority queue is taken as a fringe which is initially loaded with the intial values of route_covered, segments_covered, miles_covered, time_elapsed_covered,accidents_till_now.
A priority index will be assigned to each element of the fringe which will be used to choose the most promising states while traversing across the fringe.
Iterating over the fringe:
The first element or the element with highest priority will be popped out from the priority queue.(in this case its the initial state)
	The priority index will be calculated according to the cost function which can be either of number of segments, ditance between cities, travel time or number of accidents.
	The priority index or evaluation function  = sum of the heuristics of all moves till goal state is reached +  total cost to reach goal state.
	The heuristic chosen is haversine Distance.
The element popped out will be compared with goal state and if it is the goal state- it will be returned.
else it will be marked as visited the successors of that state will be found.
All these successors will be added to the fringe alomg with their priority values.
this process is repeated till we reach the goal state.

### Difficulties/Assumptions/Design Modifications: 
- Implementing the algorithm for the cost function = "safe" took a lot time as we need to extract the highway type which effects the accidents probability and we got stuck for a while but ere able to implement it successfully finally.
- In the case of cost function="time" we took an assumption of average maximum speed of 65 which also fills the inconsistent data in the data set.
- initially we thought of taking the heuristic function as the euclidean distance between 2 cities which is the linear distance rather than spherical distance and thus it will very much underestimate the distance cost between 2 cities. So we chose haversine formula for calculating the distance between 2 cities as the heuristic which is admissable and accurate.

# Part 3
### Choosing Teams
 * This is a Search optimization problem where we assign students to the groups based on their preferences. Students will raise a 
complaint based on the below scenarios
   
         *       student who requested a specefic group size and assigned to 
                 different group size will raise a complaint.
         *       each student send a complaint if they are assigned to a differnt group than preferred group
         *       each student who is assigned to someone whom they dont want raises a complaint.
*Goal*: Our goal is to assign groups based on student preferences minimizing total number of complaints on the above mentioned scenarios.
### Abstraction used:
The Search abstractionn is as follows

        *initial state: In this problem , intial state is the preferenece given by the students.


        *sucessor Function: our sucessor function randomly will return assigned teams from the list of all students available.


        *Goal state: Our aim is to find the  prefrence groups with min number of complaints.


        *Heuristic Function: it is the number of complaints raised: we take a successor in making it minimum.


        *State Space: It gives all the possible teams for a particular user. It wont give us a solution, but gives the overall scenario.

### Techninical Overview:

   *Readingprefernces*: This function takes the input as input file, split it and returns three lists.They are

    k:which is a list of lists(along with the user data, we have declared cost function as 0)\

    divided:This is also a list of lists with each list containing the requested team members.\

    allstudents: This has all the users who is requesting for groups.


  * cost1function: This is the cost function. which add up the complaints when ever there is a mismatach compared to the 
              user prefrences. This function takes the groups assigned and returns the total cost of complaints based on the
              below conditions.
    
                     * if the prefered length of the group is diffarent from assigned one, we add a complaint.
                     * if the preference team is not same as assigned team, Then we add a complaint for each student.
                     * if the assigned team has a member from a non-prefernce list, we add two complaints.

 * Initial_state: This function takes k from 1 st function ,users and list of prefered groups and returns random groups.

 * is_goal: This function will validate whether the teams assigned consist of all the students and returns true if all 
   the available students are assigned into teams.
   
 * Successor1: This function will generate all next possible assigned teams by picking up random choice of student from 
   the list.
   
 * Solver function: The solver function will import the raw input data into a list. It then calculates assigned cost for 
   the initial state and appends the initial state and cost variable into a fringe(priority queue). The fringe will pop 
   out the least cost assigned value and checks for is_goal state and yields the result until the time frame ends.






   






