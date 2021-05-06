# classify.py : Classify text objects into two categories
#
# Suraj Gupta Gudla - surgudla; Tarika Sadey - tsadey; Bhargav Sai Gogineni - bgoginen
#
# Based on skeleton code by D. Crandall, March 2021
#

import re
import operator
import sys

train_datalist = []
test_datalist=[]
op=[]
opstr=""
prior_probability = {}
category_count={}
word_freq = {}
likelihood_probability = {}


#function to load the training data and test data on the disk
def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to documents
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each document
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

# function to compute the prior and likelihood probabilities
def cal_freq(train_datalist, word_freq):
    for objectindex in range(len(train_datalist)):
        if train_datalist[objectindex][0] in word_freq:
            category_count[train_datalist[objectindex][0]]+=1
            for wordindex in range(1,len(train_datalist[objectindex])):
                word_freq[train_datalist[objectindex][0]][train_datalist[objectindex][wordindex]] = word_freq[train_datalist[objectindex][0]].get(train_datalist[objectindex][wordindex],0) + 1
        else:
            temp = {}
            for wordindex in range(1,len(train_datalist[objectindex])):
                temp[train_datalist[objectindex][wordindex]] = 1.0
            word_freq[train_datalist[objectindex][0]] = temp
            category_count[train_datalist[objectindex][0]] = 1
    # likelihood 
    for category in word_freq:
        likelihood_probability[category] = {}
        total = 0
        prior_probability[category] = float(category_count[category]) / len(train_datalist)
        for word in word_freq[category]:
            total = total + word_freq[category][word]
        for word in word_freq[category]:
            likelihood_probability[category][word] = float(word_freq[category][word]) / total



def object_classification(object, likelihood_probability, prior_probability):
    RHS={}
    for category in prior_probability:
        p_value = 0
        for word in range(1,len(object)):
            if p_value != 0: p_value = p_value * likelihood_probability[category].get(object[word],10**-6)
            else: p_value = likelihood_probability[category].get(object[word],10**-6)
        RHS[category] = p_value * prior_probability[category]
    return max(RHS.items(), key=operator.itemgetter(1))[0]

def classifier(train_data, test_data):
    for i in range(0, len(train_data['objects'])):
        list1 = []
        for o in str(train_data['objects'][i]).lower().split():
            word = re.sub(r'[^a-zA-Z0-9]', r'',o)
            list1.append(word)
        temp2 = list1
        train_datalist.append(" ".join([str(train_data['labels'][i]), " ".join(re.sub(' +', ' ', " ".join(temp2)).split())]).split())

    for ob in test_data['objects']:
        list2 = []
        for o1 in str(ob).lower().split():
            word1 = re.sub(r'[^a-zA-Z0-9]', r'', o1)
            list2.append(word1)
        temp3 = list2
        test_datalist.append(temp3)

    cal_freq(train_datalist, word_freq)
    templist = []
    for object in range(len(test_datalist)):
        templist.append(object_classification(test_datalist[object], likelihood_probability, prior_probability))
    return templist

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")
    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")
    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    results= classifier(train_data, test_data_sanitized)
    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))

        
