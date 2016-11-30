import urllib, os
import pandas as pd
import numpy as np
import re, nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.externals import joblib

data_list= []
data_list_test = []
for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/train/pos"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            data_list.append([file_content,"POSITIVE"])


for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/train/neg"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            data_list.append([file_content,"NEGATIVE"])


for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/test/pos"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            data_list_test.append([file_content,"POSITIVE"])


for root, dirs, files in os.walk("/Users/romilvasani/USC/CSCI544/Final Project/dataset/aclImdb/test/neg"):
    for file in files:
        if file.endswith(".txt"):
            file_open = open(os.path.join(root, file), "r")
            file_content = file_open.read()
            data_list_test.append([file_content,"NEGATIVE"])

train_data_df = pd.DataFrame(data_list_test, columns=["Text","Sentiment"])
test_data_df = pd.DataFrame(data_list, columns=["Text","Sentiment"])

print(train_data_df.Sentiment.value_counts())

print("Average words in a file: " + str(np.mean([len(s.split(" ")) for s in train_data_df.Text])))

stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    # remove non letters
    text = re.sub("[^a-zA-Z]", " ", text)
    # tokenize
    tokens = nltk.word_tokenize(text)
    # stem
    stems = stem_tokens(tokens, stemmer)
    return stems

vectorizer = CountVectorizer(
    analyzer = 'word',
    tokenizer = tokenize,
    lowercase = True,
    stop_words = 'english',
    max_features = 3000
)

corpus_data_features = vectorizer.fit_transform(train_data_df.Text.tolist() + test_data_df.Text.tolist())

corpus_data_features_nd = corpus_data_features.toarray()

log_model = LogisticRegression()
log_model = log_model.fit(X=corpus_data_features_nd[0:len(train_data_df)], y=train_data_df.Sentiment)

joblib.dump(log_model, 'logistic_model_imdb.pkl', compress=9)
joblib.dump(vectorizer, 'logistic_model_imdb_vectorizer.pkl', compress=9)

joblib.dump(corpus_data_features_nd, 'logistic_model_imdb_corpus_data_features_nd.pkl', compress=9)

joblib.dump(train_data_df, 'logistic_model_imdb_train_data_df.pkl', compress=9)

# get predictions
test_pred = log_model.predict(corpus_data_features_nd[len(train_data_df):])
actual_pred = test_data_df["Sentiment"].tolist()

print(classification_report(test_pred, actual_pred))
