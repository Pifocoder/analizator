from __future__ import division, print_function
# отключим всякие предупреждения Anaconda
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import json
import csv
import re


def train_test(file):
    reviews_train = pd.read_csv('data/train.csv')
    reviews_test = pd.read_csv('data/valid.csv')

    text_train, y_train = reviews_train['text'], reviews_train['sentiment']
    text_test, y_test = reviews_test['text'], reviews_test['sentiment']

    cv = CountVectorizer(encoding='koi8r')
    cv.fit(text_train)

    # print(len(cv.vocabulary_)) # 74849
    # print(cv.get_feature_names_out()[:50])
    # print(cv.get_feature_names_out()[50000:50050])

    X_train = cv.transform(text_train)
    X_test = cv.transform(text_test)
    y_train = y_train.astype('int')
    y_test = y_test.astype('int')

    # %%time
    logit = LogisticRegression(n_jobs=-1, random_state=7)
    logit.fit(X_train, y_train)
    print(round(logit.score(X_train, y_train), 3), round(logit.score(X_test, y_test), 3))
    from sklearn.pipeline import make_pipeline

    text_pipe_logit = make_pipeline(CountVectorizer(),
    LogisticRegression(n_jobs=-1, random_state=7))

    text_pipe_logit.fit(text_train, y_train)
    print(text_pipe_logit.score(text_test, y_test))

    from sklearn.model_selection import GridSearchCV

    param_grid_logit = {'logisticregression__C': np.logspace(-5, 0, 6)}
    grid_logit = GridSearchCV(text_pipe_logit, param_grid_logit, cv=3, n_jobs=-1)

    grid_logit.fit(text_train, y_train)
    grid_logit.best_params_, grid_logit.best_score_
    # plot_grid_scores(grid_logit, 'logisticregression__C')
    grid_logit.score(text_test, y_test)

    base = pd.read_csv(file)
    bt = base['text']
    predict_base = grid_logit.predict(bt)
    return predict_base


def normalize(file):
    mess = []
    with open(file, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for d in data:
            text = d['message']
            mess.append(re.sub(r'[^A-zА-я0-9_ .,!:;?=+№%*/&#-()]', '', text))
    with open("data/data.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['text'])
        for message in mess:
            if message != "":
                writer.writerow([message])


# file = 'data/data.csv'
# normalize(file)
# tain_test(file)
