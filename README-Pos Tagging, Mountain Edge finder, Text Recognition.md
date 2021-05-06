# a3 report

## part 1 - Part of Speech tagging

Problem statement: Find the parts of speech tags for a new sentence given you have a labelled data with pos tags already.

* Simple Algorithm:

we found the count of all pos tags occurring for each word to find their Probabilities.

We trained the data got the dictionary of words(P(w1|S), transition of words(P(N|N)) and POS probabilities (P(N)).

To perform part-of-speech tagging, we want to estimate the most-probable tags for each word Wi.

                 s∗i= arg maxsi P(Si=si|W)
                 
We just check the dictionary of word frequency for a particular words with all POS and return the maximum one.

For the ones we don't have any freq or in case of tie we return Noun as default POS.

* HMM algorithm:

For training, we Calculated the Emission and Transition Probability tables.

Emission Table - Probability of Occurrence of a word given pos tag P(tag = 't1'/word), if thata zero probability, give it a probability of 0.000000000001

Transition Probability - Probability of P(pos_tag2/pos_tag1), Ex: P('noun'/'noun')

find the maximum a posteriori (MAP) labeling for the sentence

                (s∗1, . . . , s∗N) = arg maxs1,...,sNP(Si=si|W)
                
We can solve this model by using viterbi (Dynamic Programming) using transition and emission probabilities to calculate the maximun occuring sequence.

* Complex MCMC model:

Simple Algorithm:
1)Fix the values of the observed varibles
2)set the values of the non-observed varibles randomly.
3)Randomly go through  the space of all the observed and unobserved varibles.one on each time. this is following the Markov blanket, which says most of the varibles are
  independent.
4)Repeat the process many times .
5)the probaility converges to true posterior when frequencies stop changing significantly.

Use the probability tables from previous viterbi and also caluculate the probaility of P(Sn/Sn-1,s0)

Initialize the word pos sequence to some random pos tags (Here I Initialized it to nouns).

Using Gibbs sampling sample the Probabilities each word by making all other values constant and after the healing period store the maximum occured sequences counts in a dictionary.

After sampling output the maximum occurred sequence for each word.

Note: Accuracies for complex model may vary during runs as it takes random samples.

* Posterior Probabilites:

Simple: Calculate the Posterior Probabilities of simple model as P = p(word/tag)*p(tag)

HMM: For HMM model P = p(word/tag)*prob(tag/prev_tag)

Complex_mcmc: Calculate the Posterior Probabilities of complex model as P = p(word/tag)*p(tag/prev_tag)*p(next_tag/tag)

* References:
1. http://www.cs.cmu.edu/~guestrin/Class/10701/slides/hmms-structurelearn.pdf
2. https://en.wikipedia.org/wiki/Forward%E2%80%93backward_algorithm
3. https://www.youtube.com/watch?v=dZoHsVO4F3k&t=489s
4. canvas lecture slides


## Part 2 - Mountain Finding

Problem statement: when given a image containing mountain, Identify the ridgeline, i.e. the boundary between the sky and the mountain.
Given the edge strength map that measures how strong the image gradient (local contrast) is at each point, we need to find the row number for every column which has the highest image gradient using 3 methods, namely simple, hmm - viterbi and along with human feedback.

1. In the simple model, we used numpy library to find the maximum row index in every column using the numpy.argmax() function.

2. For the second model, to populate the transition probabilites, we used viterbi algorithm with dynamic programming and back tracking method using a concept called seam carving, that gives the path (list of row indexes from start to end columns ) wsuch that when sum of image gradient is taken in the edge-strength matrix, it will be maximum.
It is based on the basic idea that a path ending at (i, j) must contain a subpath ending at either (i-1, j-1), (i-1, j), or (i-1, j+1). Here i is a row index and j is a column index. Getting an optimal solution to these 3 subproblems, the optimal solution to the comple edge strength matrix can be found.

3. when additional human feedback is given we just tweaked the previous logic, made that particular pixel's image gradient maximum, so the the resulant path will be the path that passes through the human labeled pixel always.

* Reference:

1. Course assignment on seam carving - CSCI-B 505 Applied Algorithms - Program taught by Prof. Jeremy Seik (https://iu.instructure.com/courses/1946118/assignments/11934378)
2. https://en.wikipedia.org/wiki/Forward%E2%80%93backward_algorithm

## part 3 - Reading Text

* For Training:

The courier-train.png image is used the training data for calculating the probability distribution for the pixels in the image.
The tarin-text.txt file (sample of the corpus as a approximate language model) is used for the calculation of the prior probabilities and transition probabilities. These are used in the Naive Bayes Viterbi implementation.
1) We trained the data to get the dictionary of characters(P(w1|S), transition of characters(P(N|N)).
2) For emission probabilities we used match and miss counts and calculated the character probabilities .
3) Out of the 14 * 25 blocks we considered '*' to have higher probability folowed by ' ' and lesser probability for miss data.
4) We assigned weights to each type of character and returned the highest probability for a probable character.
5) For transition prbabilities, we noticed that they were dominating, so we added a large number and divided with a small number to normalize the values. This is done to avoid the domination of transition prob in our answers. (The idea was taken from a paper mentioned in refernces.)

* For Simplified algorithm:

hit/miss ratio: Weighted sum is taken by comparing two letters pixel by pixel. If there is a match, higher weights are given and vice versa. At end average of weighted sum is taken and the corresponding letter is predicted by most matching pixels.

1) We just check the match/miss ratio for a particular char and returned the maximum one.
2) we used match and miss counts and calculated the character probabilities.
3) Out of the 14 * 25 blocks we considered '*' to have higher probability folowed by ' ' and lesser probability for miss data..
 
* For Viterbi algorithm in case of HMM:

1) The transition probabilities are calculated first which specify the chances to move from one state to the other state in the model. These are calculated from the training data (from the train-text.txt file provided as an argument) as P [S(i+1)| S(i)] where S = a valid letter in the train data.
2) A matrix of rows equal to 72(= number of train letters) and column equal to no of letters in test data is created.
3) The first column of the matrix is filled with initial probabilities calculated by matching pixel to pixel.
4) The next emission probabilities are calculated using transition probabilities and previous corresponding value.
5) We also added weights to our transition probabilities and giving maximum weight to the emission probability to get better results.

The Dynamic Programming Approach. At each state of the HMM, the probabilities are calculated by multiplying three terms,
A) Transition probability from the previous letter to current letter P(Si/Si-1): How often a letter is followed by other leters in the training file.
B) Emission probability of the current letter P(Wi/Si): Learned through the Naive Bayes.
C) Probability calculated so far P(i-1) 

6) Our each cell is of this form [probability, PrevMaxValue]
7) once we fill our veterbi matrix, we perform back tracking and find the corresponding letter where we get maximum value.
8) return the string sequence.

* References:

1. Canvas Slides
2. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.141.7177&rep=rep1&type=pdf


 

