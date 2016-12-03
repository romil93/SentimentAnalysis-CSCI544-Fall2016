import os
import glob
import re
from sys import argv
import os
from collections import defaultdict
import math
import random


def caltrain(result_dict):
    wd = defaultdict(int)
    for key in result_dict:
        for value in result_dict[key]:
            for feature in result_dict[key][value]:
                wd[feature] = 0

    b = 0
    for i in range(20):
        keys = list(result_dict.keys())
        random.shuffle(keys)
        [(key, result_dict[key]) for key in keys]

        for key in result_dict:
            sum = 0

            for value in result_dict[key]:
                y = value
                for feature in result_dict[key][value]:
                    sum = sum + (wd[feature] * result_dict[key][value][feature])
                    # print(sum)
            sum = sum + b
            print(y)
            if (y * sum) <= 0:
                for value in result_dict[key]:
                    for feature in result_dict[key][value]:
                        wd[feature] = wd[feature] + (y * result_dict[key][value][feature])
                        # print(wd[feature])

                b = b + y
                # print(wd)
    model = open("per_model.txt", "w", encoding='latin-1')
    model.write("biasword ")
    model.write(str(b))
    model.write("\n")
    for word in wd:
        model.write(word)
        model.write(" ")
        model.write(str(wd[word]))
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
poslim = 0
neglim = 0

for root, dirs, files in os.walk('C:/Users/seems/Desktop/imdb/train/pos'):
    for name in files:

        filename = os.path.join(root, name)
        file = open(filename, 'r', encoding='latin-1')
        fileread = file.read()

        # fileread = fileread.encode('utf-8').strip()

        new_str = re.sub('[^a-zA-Z\n\.]', ' ', fileread)
        n_space = re.sub(' +', ' ', new_str)
        # n_space = re.sub('\.\.+', ' ', n_space)
        # Remove single dots
        # n_space = re.sub('\.', '', n_space)
        fileread=new_str.lower()
        # fileread = fileread.replace('\n','')
        wordsplit = fileread.split()

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

        # new_str = re.sub('[^a-zA-Z\n\.]', ' ', fileread)
        # n_space = re.sub(' +', ' ', new_str)
        # n_space = re.sub('\.\.+', ' ', n_space)
        # Remove single dots
        # n_space = re.sub('\.', '', n_space)
        # fileread=new_str.lower()
        # fileread = fileread.replace('\n','')
        wordsplit = fileread.split()
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




