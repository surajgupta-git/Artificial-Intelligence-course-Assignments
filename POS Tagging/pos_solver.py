###################################
# CS B551 Spring 2021, Assignment #3
#
# surgudla-bgoginen-tsadey
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import numpy as np


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):

        self.part_of_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        self.speech_count = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0, 'num': 0, 'pron': 0,
                             'prt': 0,
                             'verb': 0, 'x': 0, '.': 0}
        self.speech_prob = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0, 'num': 0, 'pron': 0, 'prt': 0,
                            'verb': 0, 'x': 0, '.': 0}
        self.word_count = {}
        self.word_prob = {}
        self.speech_word_count = {}
        self.start_word_dict = {}
        self.transition_count_dict = {}
        self.transition_prob_dict = {}
        self.emission_prob = {}

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    #The below posterior function caluclates the final probability based on wheather it is simple, complex or HMM.
    def posterior(self, model, sentence, label):
        #SIMPLE: We just need to find the probability of the speech(Unobseravable varible)given words(obserbale varibles)
        if model == "Simple":
            Posterior_Prob = 0
            # P = prob(word/speech)*prob(speech)
            for num in range(len(sentence)):
                Posterior_Prob += math.log(self.speech_prob.get(label[num], 0.000000000001)) + \
                                  math.log(self.emission_prob.get((sentence[num], label[num]), 0.000000000001))
            return Posterior_Prob
        #HMM: The following depends on the initial probabilities of the previous word, emission probaility of the word and transition from previous state to this state

        elif model == "HMM":
            Posterior_Prob = 0
            # P = Prob(word/speech)*prob(speech/prev_speech)
            for num in range(len(sentence)):
                if num == 0:
                    Posterior_Prob += math.log(self.emission_prob.get((sentence[num], label[num]), 0.000000000001)) + \
                                      math.log(self.transition_prob_dict.get(('start', label[num])))
                else:
                    Posterior_Prob += math.log(self.emission_prob.get((sentence[num], label[num]), 0.000000000001)) + \
                                      math.log(self.transition_prob_dict.get((label[num - 1], label[num])))
            return Posterior_Prob
       #Complex: While sampling the particular unobserable varible we make it conditionally dependent on all other observed and unobserved varibles
       # we do it many number of times and ignore the first few times because it leaves the redundant ones and record the consistent ones.
        elif model == "Complex":
            # P = p(word/speech)*p(speech/prev_speech)*p(next_speech/speech)
            Posterior_Prob = 0
            for i in range(len(sentence)):
                if len(sentence) == 1:
                    Posterior_Prob += math.log(self.emission_prob.get((sentence[i], label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get(('start', label[i]), 0.00000000000000001))
                elif i == 0:
                    Posterior_Prob += math.log(self.emission_prob.get((sentence[i], label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get(('start', label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get((label[i], label[i + 1]), 0.00000000000000001))
                elif i == len(sentence) - 1:
                    Posterior_Prob += math.log(self.emission_prob.get((sentence[i], label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get((label[i - 1], label[0]), 0.00000000000000001)) \
                                      + math.log(
                        self.emission_prob.get((sentence[i], label[i - 1]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get((label[i], label[i - 1]), 0.00000000000000001))
                else:
                    Posterior_Prob += math.log(self.emission_prob.get((sentence[i], label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.emission_prob.get((sentence[i - 1], label[i - 1]), 0.00000000000000001)) \
                                      + math.log(
                        self.emission_prob.get((sentence[i], label[i - 1]), 0.00000000000000001)) \
                                      + math.log(
                        self.emission_prob.get((sentence[i + 1], label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.emission_prob.get((sentence[i + 1], label[i + 1]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get((label[i - 1], label[i]), 0.00000000000000001)) \
                                      + math.log(
                        self.transition_prob_dict.get((label[i], label[i + 1]), 0.00000000000000001))

            return Posterior_Prob
        else:
            print("Unknown algo!")


    # Do the training!
    #
    def train(self, data):
        pos_list = []
        for word, pos in data:
            pos_list.append(pos)
        # Transition probabilities
        for pos in pos_list:
            for i in range(len(pos)):
                if i == 0:
                    if ('start', pos[i]) not in self.transition_count_dict:
                        self.transition_count_dict['start', pos[i]] = 1
                    else:
                        self.transition_count_dict['start', pos[i]] += 1
                elif i == len(pos) - 1:
                    if (pos[i - 1], pos[i]) not in self.transition_count_dict:
                        self.transition_count_dict[pos[i - 1], pos[i]] = 1
                    else:
                        self.transition_count_dict[pos[i - 1], pos[i]] += 1
                else:
                    if (pos[i - 1], pos[i]) not in self.transition_count_dict:
                        self.transition_count_dict[pos[i - 1], pos[i]] = 1
                    else:
                        self.transition_count_dict[pos[i - 1], pos[i]] += 1

        dict_key = []
        for key in self.transition_count_dict:
            dict_key.append(key)
        dict_key.sort()

        # Parts of Speech, word, word-pos count
        for word, pos in data:
            for w, p in zip(word, pos):
                self.speech_count[p] += 1
                if w in self.word_count.keys():
                    self.word_count[w] += 1
                else:
                    self.word_count[w] = 1
                if w in self.speech_word_count.keys():
                    self.speech_word_count[w][p] += 1
                else:
                    self.speech_word_count[w] = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0,
                                                 'num': 0, 'pron': 0, 'prt': 0, 'verb': 0, 'x': 0, '.': 0}
                    self.speech_word_count[w][p] += 1

        # Part of Speech Probabilities
        totalSum_pos_count = 0
        for pos in self.part_of_speech:
            totalSum_pos_count += self.speech_count[pos]
        for pos in self.part_of_speech:
            self.speech_prob[pos] = round((self.speech_count[pos] / totalSum_pos_count), 16)

        for i in dict_key:
            if i[0] == 'start':
                if i not in self.transition_prob_dict:
                    self.transition_prob_dict[i] = round((self.transition_count_dict[i] / len(data)), 16)
            else:
                sum = self.speech_count[i[0]]
                if i not in self.transition_prob_dict:
                    self.transition_prob_dict[i] = round((self.transition_count_dict[i] / sum), 16)

        # Word Probabilities
        total_word_sum = 0
        word_key_dict = []
        for keys in self.word_count:
            word_key_dict.append(keys)
        for word in word_key_dict:
            total_word_sum += self.word_count[word]
        for word in word_key_dict:
            self.word_prob[word] = round((self.word_count[word] / total_word_sum), 16)

        # Emission Probabilities
        for pos_word in self.speech_word_count.keys():
            for pos in self.part_of_speech:
                if self.speech_word_count[pos_word][pos] == 0:
                    self.emission_prob[pos_word, pos] = 0.00000000000000001
                else:
                    self.emission_prob[pos_word, pos] = round(self.speech_word_count[pos_word][pos] /
                                                              self.speech_count[pos], 16)

        self.simplified_dict = {}
        # For Simplified
        for pos_word in self.speech_word_count.keys():
            for pos in self.part_of_speech:
                if self.speech_word_count[pos_word][pos] == 0:
                    self.simplified_dict[pos_word, pos] = 0.00000000000000001
                else:
                    self.simplified_dict[pos_word, pos] = round((self.emission_prob[pos_word,pos] * self.speech_prob[pos])
                                                                / self.word_prob[pos_word], 16)
        pass

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    def simplified(self, sentence):
        part_of_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        parts_of_speech = []
        speech_temp = ''
        for word in sentence:
            value = 0
            if word in self.word_count:
                for pos in part_of_speech:
                    if self.simplified_dict[word, pos] > value:
                        value = self.simplified_dict[word, pos]
                        speech_temp = pos
                parts_of_speech.append(speech_temp)
            else:
                parts_of_speech.append('noun')
        return parts_of_speech

    def hmm_viterbi(self, sentence):
        viterbi_table = np.zeros(12 * len(sentence)).reshape(12, len(sentence))
        l = len(sentence) - 1
        viterbi_path = np.zeros(12 * l).reshape(12, l)
        part_of_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        c = 0
        for i in range(len(sentence)):
            if i == 0:
                for j in range(0, 12):
                    FirstWord = math.log(self.emission_prob.get((sentence[i], part_of_speech[j]), 0.00000000000000000001)) + \
                                math.log(self.transition_prob_dict.get(('start', part_of_speech[j]), 0.0000000000000000001))
                    viterbi_table[j][0] = FirstWord
            else:
                for j in range(0, 12):
                    em_prob = math.log(self.emission_prob.get((sentence[i], part_of_speech[j]), 0.00000000000000000001))
                    max_tran_prev_state = []
                    for num in range(0, 12):
                        trans_prob = math.log(self.transition_prob_dict.get((part_of_speech[num], part_of_speech[j]),
                                                                            0.00000000000000000001))
                        value = viterbi_table[num][c - 1] + trans_prob
                        max_tran_prev_state.append(value)
                    max_value = max(max_tran_prev_state)  # Store the max value of the transitions.
                    max_index = max_tran_prev_state.index(max_value)  # Store the index of the max value.
                    viterbi_path[j][c - 1] = max_index  # Save the value in route.
                    viterbi_table[j][c] = em_prob + max_value  # update the viterbi table for the second word.
            c += 1

        viterbi_path = viterbi_path.astype('int')
        index = np.argmax(viterbi_table, axis=0)[-1]
        label = [index]
        c = len(sentence) - 2
        while c >= 0:
            index = viterbi_path[index][c]
            label.append(index)
            c -= 1
        label = label[::-1]
        parts_of_speech = [part_of_speech[i] for i in label]
        return parts_of_speech

    def random_unobserved_variable(self,sentence):
        label = self.simplified(sentence)
        return label

    def probability(self,prob_list):
        probability_list = [math.exp(i) for i in prob_list]
        Total_sum = sum(probability_list)
        for i in range (len(probability_list)):
            probability_list[i] = probability_list[i]/Total_sum
        return probability_list

    def complex_mcmc(self, sentence):
        parts_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        # we have to fix the random POS for all the words,so instaed of hardcoding it, we have called the simple model to do the work.
        # According to gibs sampling, if we have make samping n times , we have to ignore 3/4n and record the 1/4n. we dont need to worry about the healing and
        #burning concept as we have fixed the somewhat correct pos for the words with the help of simple model.
        random_pos = self.random_unobserved_variable(sentence)
        final_count = {}

        for i in range(500):
            for word in range(len(sentence)):
                prob_list1 = []
                #if the sentance cosists of just one word
                if len(sentence) == 1:
                    for pos in parts_speech:
                        P = [math.log(self.emission_prob.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get(('start', pos), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)
                #sampling for the First POS
                elif word == 0:
                    for pos in parts_speech:
                        P = [math.log(self.emission_prob.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get(('start', pos), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get((pos, random_pos[word + 1]), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)
                #Sampling for the last POS
                elif word == len(random_pos) - 1:
                    for pos in parts_speech:
                        P = [math.log(self.emission_prob.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get((random_pos[word - 1], random_pos[0]), 0.00000000000000001))
                             + math.log(self.emission_prob.get((sentence[word], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get((pos, random_pos[word - 1]), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)
                #Sampling for all the middle words.
                else:
                    for pos in parts_speech:
                        P = [math.log(self.emission_prob.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.emission_prob.get((sentence[word - 1], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.emission_prob.get((sentence[word], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.emission_prob.get((sentence[word + 1], random_pos[word]), 0.00000000000000001))
                             + math.log(self.emission_prob.get((sentence[word + 1], random_pos[word + 1]), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get((random_pos[word - 1], pos), 0.00000000000000001))
                             + math.log(self.transition_prob_dict.get((pos, random_pos[word + 1]), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)

                possible_prob = self.probability(prob_list1)
                #Now we are fliping a coin to sample each word of a sentence.
                x = random.uniform(0,1)
                max_value = 0
                for p in range(len(possible_prob)):
                    max_value += possible_prob[p]
                    if max_value > x:
                        random_pos[word] = self.part_of_speech[p]
                        break
                for i in range(len(random_pos)):
                    if (i,random_pos[i]) not in final_count:
                        final_count[i, random_pos[i]] = 1
                    else:
                        final_count[i,random_pos[i]] += 1
        labels = []
        for i in range(len(random_pos)):
            max = 0
            speech = ''
            for pos in self.part_of_speech:
                if (i, pos) in final_count:
                    if max <= final_count[i,pos]:
                        max = final_count[i,pos]
                        speech = pos
            labels.append(speech)
        return labels

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
