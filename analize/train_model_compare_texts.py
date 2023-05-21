import pandas as pd
from sklearn.linear_model import LinearRegression

import os
def get_model():

    with open (os.path.abspath('analize/datasets/log_reg_train.csv')) as log_reg_train:

        df = pd.read_csv(log_reg_train, delimiter=',')
        X = df[['nodist_1', 'nodist_2', 'nodist_3', 'dist', 'types_same']]
        y = df[['target']]
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

        #initiate linear regression model
        model = LinearRegression()
        model.fit(X.values, y.values)

        return model

# print(get_model())