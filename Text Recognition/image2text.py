#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: surgudla-tsadey-bgoginen
# (based on skeleton code by D. Crandall, Oct 2020)
#
import math
from PIL import Image
import sys

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
TRAIN_LETTERS_G = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH)]) for y in
                    range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}


#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)


# training the data to get transition,start and all character probabilities
def train():
    model = []
    tran_dictionary = {}
    startChar_dict = {}
    character_dict = {}

    for line in open(train_txt_fname, 'r'):
        model_data = tuple([data for data in line.split()])
        model += [model_data]
    file = open(train_txt_fname, 'r')
    model1 = [line1.strip() for line1 in file]

    for model_data in model:
        # Start character dictionary
        for data in model_data[0]:
            if data[0] in train_letters:
                if data[0] not in startChar_dict:
                    startChar_dict[data[0]] = 1
                else:
                    startChar_dict[data[0]] += 1

        data = " ".join(model_data)
        # Transition count dictionary
        for i in range(len(data)):
            for j in range(1, len(data)):
                if (data[i], data[j]) in tran_dictionary:
                    tran_dictionary[data[i], data[j]] += 1
                else:
                    tran_dictionary[data[i], data[j]] = 1
    # Count of all Characters
    for i in range(len(model1)):
        for j in range(len(model1[i])):
            if model1[i][j] in character_dict:
                character_dict[model1[i][j]] += 1
            else:
                character_dict[model1[i][j]] = 1
    # Transition probabilities
    for t1 in TRAIN_LETTERS_G:
        for t2 in TRAIN_LETTERS_G:
            if (t1, t2) not in tran_dictionary:
                tran_dictionary[t1, t2] = 0.000000000001
            else:
                tran_dictionary[t1, t2] = tran_dictionary[t1, t2] / character_dict[t1]

    return [startChar_dict, character_dict, tran_dictionary]


# Calculate probabilities for simple model by considering *, ' '  and miss probabilities
# We assigned weights to each label by approximating their occurance in the data
def Simpleletter(letter):
    probable = {}
    for char in TRAIN_LETTERS_G:
        match, miss, blankCount = 0, 1, 0
        for i in range(len(letter)):
            for j in range(len(letter[i])):
                if letter[i][j] == ' ' and train_letters[char][i][j] == ' ':
                    blankCount += 1
                    pass
                else:
                    if letter[i][j] == train_letters[char][i][j] == '*':
                        match += 1
                    else:
                        miss += 1
        probable[char] = (0.85 * match + 0.1 * blankCount + 0.05 * miss) / (CHARACTER_WIDTH * CHARACTER_HEIGHT)
    return max(probable.items(), key=lambda x: x[1])[0]


def simplified(test_letters):
    resultString = ''
    for letter in test_letters:
        resultString += Simpleletter(letter)
    return resultString


# Calculating the probabilities for HMM_Viterbi model
def viterbi_prob(letter, test_letters):
    match, miss, blankCount = 0, 1, 0
    for i in range(CHARACTER_HEIGHT):
        for j in range(CHARACTER_WIDTH):
            if test_letters[i][j] == ' ' and train_letters[letter][i][j] == ' ':
                blankCount += 1
            elif test_letters[i][j] == train_letters[letter][i][j] == '*':
                match += 1
            elif test_letters[i][j] == train_letters[letter][i][j] == '*':
                miss += 1
    prob = (0.85 * match + 0.1 * blankCount + 0.05 * miss) / (CHARACTER_WIDTH * CHARACTER_HEIGHT)
    return prob


def HMM_Viterbi(test, tran_dict):
    viterbi_table = []
    l1 = []
    for i in range(len(TRAIN_LETTERS_G)):
        FirstWord = math.log(viterbi_prob(TRAIN_LETTERS_G[i], test_letters[0]))
        l1.append(FirstWord)
    viterbi_table.append(l1)

    for i in range(1, len(test)):
        l1 = []
        for j in range(len(TRAIN_LETTERS_G)):
            em_prob = math.log(viterbi_prob(TRAIN_LETTERS_G[j], test[i]))  # emission probabilities
            max_tran_prev_state = 0
            for k in range(len(TRAIN_LETTERS_G)):
                # transition probabilities
                trans_prob = math.log(tran_dict.get((TRAIN_LETTERS_G[j], TRAIN_LETTERS_G[k]), 0.000000000001))
                value = viterbi_table[i - 1][k] + trans_prob
                # Store the max value of the transitions.
                if value > max_tran_prev_state:
                    max_tran_prev_state = value
            # assign prob as log sum of emission and max of transition probabilities
            v_value = max_tran_prev_state + em_prob
            l1.append(v_value)
        viterbi_table.append(l1)
    # use backtracking to find the most probable characters
    label = ''
    for i in range(len(test)):
        index = 0
        temp = -(math.pow(10, 5))
        for j in range(len(TRAIN_LETTERS_G)):
            if temp < viterbi_table[i][j]:
                temp = viterbi_table[i][j]
                index = j
        label += TRAIN_LETTERS_G[index]
    return label


[startChar_dict, character_dict, tran_dictionary] = train()

print("Simple: " + simplified(test_letters))
print("   HMM: " + HMM_Viterbi(test_letters, tran_dictionary))
