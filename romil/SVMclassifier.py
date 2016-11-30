from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import csv, os
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import random
from sklearn import metrics
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.svm import SVC, LinearSVC

tokenizer = RegexpTokenizer(r'\w+')
stop = stopwords.words('english')


data = {"text":[], "class":[]}

for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/train/pos"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            tokens = []
            token = tokenizer.tokenize(file_content)
            for i in token:
                if i not in stop:
                    tokens.append(i)

            value = " ".join(tokens)
            data["text"].append(value)
            data["class"].append("POSITIVE")


for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/train/neg"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            tokens=[]
            token = tokenizer.tokenize(file_content)
            for i in token:
                if i not in stop:
                    tokens.append(i)

            value = " ".join(tokens)
            data["text"].append(value)
            data["class"].append("NEGATIVE")

for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/test/pos"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            tokens = []
            token = tokenizer.tokenize(file_content)
            for i in token:
                if i not in stop:
                    tokens.append(i)

            value = " ".join(tokens)
            data["text"].append(value)
            data["class"].append("POSITIVE")


for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/test/neg"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            tokens=[]
            token = tokenizer.tokenize(file_content)
            for i in token:
                if i not in stop:
                    tokens.append(i)

            value = " ".join(tokens)
            data["text"].append(value)
            data["class"].append("NEGATIVE")

length = len(data["text"])
sample = random.sample(range(0, length), length)
data["text"] = [data["text"][i] for i in sample]
data["class"] = [data["class"][i] for i in sample]

pipeline = Pipeline([
	('vectorizer',  CountVectorizer(ngram_range=(1, 2))),
	# ('classifier',  MultinomialNB()) ])
	#('classifier',  SVC(kernel='linear'))
    ('classifier',  LinearSVC())
    #('classifier',  SGDClassifier(loss='hinge', penalty='l2',
    #                                    alpha=1e-3, n_iter=5, random_state=42))
                                          ])

k_fold = KFold(n=len(data["text"]), n_folds=5)
new_data_text = numpy.asarray(data['text'])
new_data_class = numpy.asarray(data['class'])
scores = []

for train_indices, test_indices in k_fold:
    train_text = new_data_text[train_indices]
    train_y = new_data_class[train_indices]
    test_text = new_data_text[test_indices]
    test_y = new_data_class[test_indices]
    pipeline.fit(train_text, train_y)

    predicted = pipeline.predict(test_text)
    score = pipeline.score(test_text, test_y)
    scores.append(score)
    
    print(metrics.classification_report(test_y, predicted, target_names=['POSITIVE', 'NEGATIVE']))
score = sum(scores) / len(scores)
print("Mean Accuracy: " + str(score))
