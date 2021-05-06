### ASSIGNMENT 1 REPORT
###### Course: Elements of AI(SP21-BL-CSCI-B551-37653)
###### CS B551 - Assignment 2: Games
###### Name: Bhargav Sai Gogineni, Suraj Gupta Gudla, Tarika Sadey
###### UserName: bgoginen-surgudla-tsadey
###### GIT repo: bgoginen-surgudla-tsadey-a2

------------------------------------------------------------------------------------------------------------------------ 
### PART 1: PIKACHU
Finding the best move of a player from a given board state that was played by the opponent player.

#### Search Abstraction:
* Initial State: Given Current board.
* Terminal State: If all pieces of opposite player are killed or the search depth is reached.
* Successors: List of all the valid moves for all the pieces on the board for the current player
* Evaluation function: 3 *(white pikachus - black pikachus) + 1 * (white pichus - black pichus).

#### Overview of Solution:
* We have employed the minimax algorithm with alpha-beta pruning along with iterative deepening search to form the 
  search tree and then back-up up the values upwards that are calculated using the evaluation function applied to the 
  leaf states at that particular depth.

* Our successor function return all possible next moves for a given player (either 'w' or 'b').

* We chose the default alpha and beta values as -100000000 and +10000000 respectively, then Back-up of values upwards 
  using the functions:
	def maxvalue(successor, alpha, beta, depth, player, depthlimit,N):
	def minvalue(successor, alpha, beta, depth, player, depthlimit,N):

* In case our search tree terminal state is encountered when the search tree goes till the complete depth i.e. till the 
  leaf by checking if either the total count of black pieces or white pieces is zero.

* We defined the evaluation function as a sum of weighted features where weight of 3 was given to the difference of 
  white and black Pikachus and weight of 1 to the difference of white and black pichus.

* In the core minimax algorithm, we have used a max heap to get the maximum alpha value for a state.

* At the start we considered the current player as Max player and the opposite player as Min player, then we calculate 
  the max of all the beta which in turn are the minimum of alpha (recurrence). We started with depth 2 for finding the 
  search tree and yield the output and if there is still time remaining from the permissible time limit then we increase 
  the depth by one and search again for better output and yield the new output.

#### Difficulties Faced:
* We faced difficulty in writing the successor function especially during the corner cases when a pichu evolves into a 
  pikachu.

* Another thing where we were confused is the code execution getting stopped after a specific time-limit without reaching 
  the terminal state.In such case after a lot of brain storming we were able to figure out the algorithm by writing an 
  evaluation function that calculates an utility value for all states in that depth and employing iterative deepening 
  method that yields a better next move  for every depth
  
------------------------------------------------------------------------------------------------------------------------ 
### PART 2 : THE GAME OF SEBASTIAN
* The problem poses a one player game of luck and skill of rolling five dice and write an algorithm to obtain a maximum
  score within 13 chances provided we need to choose optimum re-rolls of specific dice using none or 2 more chances per 
  specific turn.
  
* Within one game of thirteen turns, we need to assign dice roll to specific categories in the score card given a 
  category can be only assigned once per a game.
  
#### Problem Abstraction:
* We have implemented expectation probability concept to obtain the optimal best score using the below described 
  technique.

* For each first roll of random selection of dice we have considered all possible combinations of die roll and 
  calculated expected score for each combination.
  
* The expected score is obtained by assigning the die combination to all possible 13 categories and storing the 
  category and its respective score into a dictionary.
  
* We then take the best score from the sorted dictionary and send it to max_layer function. We then compare each expected
  score and store the max score for each combination. After all the iterations we send back the best possible re-roll
  indices to be rolled in the second chance. 
  
* Similar process is followed for the second roll.

* The third roll function gives the best category from the list of available unassigned categories in each game for a 
  given best die combination after second re-roll.
  
* The minimum, maximum and mean scores are then calculated after the player plays 100 games giving us the desired output.

#### Problems Faced:
* Assignment of best category for a given turn has proved to be quite a task when calculating the max expected value of
  each die roll combination which we have overcome by eliminating the already assigned categories from the list.
  
* We have eliminated the duplicate combinations of die roll to optimize time complexity of the code.

------------------------------------------------------------------------------------------------------------------------
### PART 3: DOCUMENT CLASSIFICATION
Tweet Classification: Using Naive Bayes Law and bag of words assumption, we created a Classification model and trained 
it using the training data and predicted the class to which an object of words belongs to.

#### Problem Statement:
* We are using Multinomial Naive Bayes Classification wherein we create a multinomial distribution of words for each 
  class present in the training data and then predict the class to which the Object of words from the testing data 
  belongs to.

* Using the labels already given in the test data, we also find the accuracy of the classification model.We achieved an 
  accuracy of around 84 %.
	
* Firstly, we are loading the training and testing data files on the disk into 2 separate lists and then we are 
  pre-processing/cleaning the training data as well as the sanitized test data (test data without labels) by removing 
  the special characters, extra spaces, and carriage return using regex. 
	
* Secondly, we are considering all the words present in the training data after pre-processing to create a multinomial 
  distribution for each city. 
	
* Also When we encounter a word not present in a class we punish(multiply by a pseudo count around 10**-6) that class 
  by a factor. here we are smoothening the data so that no prob value is zero. 
(Reference: https://medium.com/syncedreview/applying-multinomial-naive-bayes-to-nlp-problems-a-practical-explanation-4f5271768ebf)
	
* We used Naive Bayes law To find how likely it is that an object belongs to a particular class, which states that:
  P(Posterior) prob i.e. P(Class | object of words ) = P(Likelihood) prob * P(Prior) prob 
  where the Prior prob of each class is equal to the ratio of the number of objects present in that particular category 
  to the total num of objects in the data set and likelihood probability of a word given category is the number of 
  repetitions of that particular word in that category to the total number of words in that category.We have calculated 
  the above by creating a dictionary word_freq[category][word]
	
* The class/category which gets the maximum P(Posterior) probability value for an object will be assigned to that object.
	
* Here we are ignoring the denominator (prior prob of each class) of the Bayes law because it will be constant for all 
  classes in the given data set.

* So, we are only maximizing over the numerator for all the tweets and then selecting the maximum from that.

* Also as all the words are independent of each other P(w1,w2,w3,.....) = P(w1) * P(w2) * P(w3) * ....



  

