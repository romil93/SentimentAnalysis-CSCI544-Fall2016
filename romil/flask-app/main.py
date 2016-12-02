from flask import Flask, render_template, redirect, request
from sklearn.externals import joblib
import urllib, os
import pandas as pd
import numpy as np
import re, nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import random

app = Flask(__name__)

@app.route('/result', methods = ['POST', 'GET'])
def result():
    return render_template("results.html")

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        review = request.form['review'].replace('\n','').strip()
        log_model = joblib.load('logistic_model_imdb.pkl')
        train_data_df = joblib.load('logistic_model_imdb_train_data_df.pkl')

        stemmer = PorterStemmer()
        def stem_tokens(tokens, stemmer):
            stemmed = []
            for item in tokens:
                stemmed.append(stemmer.stem(item))
            return stemmed

        def tokenize(text):
            text = re.sub("[^a-zA-Z]", " ", text)
            tokens = nltk.word_tokenize(text)
            stems = stem_tokens(tokens, stemmer)
            return stems

        vectorizer = CountVectorizer(
            analyzer = 'word',
            tokenizer = tokenize,
            lowercase = True,
            stop_words = 'english',
            max_features = 2000
        )

        data_list_test = [[review]]
        test_data_df = pd.DataFrame(data_list_test, columns=["Text"])

        corpus_data_features = vectorizer.fit_transform(train_data_df.Text.tolist() + test_data_df.Text.tolist())

        corpus_data_features_nd = corpus_data_features.toarray()

        test_pred = log_model.predict(corpus_data_features_nd[len(train_data_df):])

        spl = [0]

        for text, sentiment in zip(test_data_df.Text[spl], test_pred[spl]):
            print(sentiment, text)

        return test_pred[0] + " " + review 
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)
