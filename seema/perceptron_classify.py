import os
import re
import math
from sys import argv

from collections import defaultdict
from nltk.corpus import stopwords


def createdict():
    count_documents = 0

    classified_neg = 0
    classified_pos = 0
    belongs_neg = 0
    belongs_pos = 0
    correct_classify_neg = 0
    correct_classify_pos = 0
    wd = {}

    file = open('per_model.txt', 'r', encoding='latin1')

    for line in file:
        # print line
        y = line.strip().split()
        # print y
        # print line

        if y[0] == 'biasword':
            b = y[1]

        elif y[0] == 'betaword':
            b = y[1]

            # print totword

        else:
            # print result_dict

            wd[y[0]] = y[1]

    result_dict = {}

    model = open('per_output.txt', "w")

    for root, dirs, files in os.walk('C:/Users/seems/Desktop/imdb/test'):
        for nam in files:

            if nam.endswith('.txt'):
                count_documents = count_documents + 1

            filename = os.path.join(root, nam)
            file = open(filename, 'r', encoding='latin-1')
            fileread = file.read()

            if root == 'C:/Users/seems/Desktop/imdb/test\pos':
                belongs_pos = belongs_pos+1
            if root == 'C:/Users/seems/Desktop/imdb/test\\neg':
                belongs_neg=belongs_neg+1

            # new_str = re.sub('[^a-zA-Z\n\.]', ' ', fileread)
            # n_space = re.sub(' +', ' ', new_str)
            # n_space = re.sub('\.\.+', ' ', n_space)
            # Remove single dots
            # n_space = re.sub('\.', '', n_space)
            # n_space = fileread.lower()
            # fileread = fileread.replace('\n', '')
            result_dict[nam] = {}
            wordsplit = fileread.split()
            #filtered_words = [word for word in wordsplit if word not in stopwords.words('english')]
            sum = 0

            for w in wordsplit:
                if w == ' ':
                    break
                elif w not in result_dict[nam]:
                    result_dict[nam][w] = 1
                else:
                    result_dict[nam][w] = result_dict[nam][w] + 1

                if w in wd:
                    # print(wd[w])
                    sum = sum + (result_dict[nam][w] * float(wd[w]))
            alpha = sum + float(b)

            if alpha > 0:

                model.write('negative')
                model.write(' ')
                model.write(nam)
                #print('negative',fileread)
                #print('\n')
                classified_neg = classified_neg + 1
                if root == 'C:/Users/seems/Desktop/imdb/test\\neg':
                    correct_classify_neg = correct_classify_neg + 1


            else:
                model.write('positive')
                model.write(' ')
                model.write(nam)
                #print('positive', fileread)
                #print('\n')
                classified_pos = classified_pos + 1
                if root == 'C:/Users/seems/Desktop/imdb/test\pos':
                    correct_classify_pos = correct_classify_pos + 1

            model.write("\n")

    model.close()

    precision_neg = correct_classify_neg / classified_neg
    recall_neg = correct_classify_neg/ belongs_neg
    fscore_neg = 2 * precision_neg * recall_neg / (precision_neg + recall_neg)

    precision_pos = correct_classify_pos / classified_pos
    recall_pos = correct_classify_pos / belongs_pos
    fscore_pos = 2 * precision_pos * recall_pos / (precision_pos + recall_pos)

    print(precision_neg)
    print(recall_neg)
    print(fscore_neg)

    print(precision_pos)
    print(recall_pos)
    print(fscore_pos)


createdict()
