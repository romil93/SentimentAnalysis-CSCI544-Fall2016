import os
import glob
import re
from sys import argv

import os
from collections import defaultdict
from nltk.corpus import stopwords
import math
import random



def caltrain(result_dict):
    wd = defaultdict(int)
    ud = defaultdict(int)
    for key in result_dict:
        for value in result_dict[key]:
           for feature in result_dict[key][value]:
                wd[feature]= 0
                ud[feature] = 0


    b = 0
    beta = 0
    c=1
    for i in range(30):
        keys_val =  list(result_dict.keys())
        random.shuffle(keys_val)
        [ (k, result_dict[k]) for k in keys_val]
        for key in result_dict:
            sum = 0

            for value in result_dict[key]:
                y=value
                for feature in result_dict[key][value]:
                    sum = sum + (wd[feature]*result_dict[key][value][feature])
                #print(sum)
            sum = sum+b

            if (y*sum)<=0:
                for value in result_dict[key]:
                    for feature in result_dict[key][value]:
                        wd[feature] = wd[feature]+(y*result_dict[key][value][feature])
                        ud[feature] = ud[feature]+(y*c*result_dict[key][value][feature])
                    #print(wd[feature])

                b = b+y
                beta = beta + (y*c)
            c = c+1
    for key in result_dict:
        for value in result_dict[key]:
            for feature in result_dict[key][value]:
                ud[feature]=wd[feature]-((1/c)*ud[feature])
    beta = b - ((1/c)*beta)
        #print(wd)
    model = open("per_model.txt", "w", encoding="latin1")

    model.write("betaword ")
    model.write(str(beta))
    model.write("\n")

    for word in ud:

        model.write(word)
        model.write(" ")
        model.write(str(ud[word]))
        model.write("\n")
    model.close()

words = []
poscount = 0
negcount = 0
totword = 0
result_dict = {}
posdocs = 0
negdocs = 0
totdocs = 0
poslim=0
neglim=0


for root, dirs, files in os.walk('C:/Users/seems/Desktop/imdb/train/pos'):
    for name in files:

        filename = os.path.join(root, name)
        file = open(filename, 'r', encoding='latin-1')
        fileread = file.read()

        # fileread = fileread.encode('utf-8').strip()

        new_str = re.sub('[^a-zA-Z\n\.]', ' ', fileread)
        #n_space = re.sub(' +', ' ', new_str)
        n_space = re.sub('\.\.+', ' ', n_space)
        # Remove single dots
        #n_space = re.sub('\.', '', n_space)
        fileread=n_space.lower()
        #fileread = fileread.replace('\n','')
        wordsplit = fileread.split()
        wordsplit = [word for word in wordsplit if word not in stopwords.words('english')]

        # print (wordsplit)
        result_dict[name] = {}

        y_val = -1
        result_dict[name][y_val] = {}
        for w in wordsplit:
            if w == ' ':
                break
            elif w not in result_dict[name][y_val]:
                result_dict[name][y_val][w] = 1
            else:
                result_dict[name][y_val][w] = result_dict[name][y_val][w] + 1
        #print(result_dict)

for root, dirs, files in os.walk('C:/Users/seems/Desktop/imdb/train/neg'):
    for name in files:

        filename = os.path.join(root, name)
        file = open(filename, 'r', encoding='latin-1')
        fileread = file.read()

        # fileread = fileread.encode('utf-8').strip()

        new_str = re.sub('[^a-zA-Z\n\.]', ' ', fileread)
        n_space = re.sub(' +', ' ', new_str)
        #n_space = re.sub('\.\.+', ' ', n_space)
        # Remove single dots
        #n_space = re.sub('\.', '', n_space)
        fileread=n_space.lower()
        # fileread = fileread.replace('\n','')
        wordsplit = fileread.split()
        filtered_words = [word for word in wordsplit if word not in stopwords.words('english')]

        # print (wordsplit)
        result_dict[name] = {}
        y_val = 1
        result_dict[name][y_val] = {}

        for w in wordsplit:
            if w == ' ':
                break
            elif w not in result_dict[name][y_val]:
                result_dict[name][y_val][w] = 1
            else:
                result_dict[name][y_val][w] = result_dict[name][y_val][w] + 1

caltrain(result_dict)
#print(result_dict)
#print(result_dict)


