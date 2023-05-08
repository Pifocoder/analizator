import pandas as pd

def get_model():
    df = pd.read_csv('datasets/log_reg_train.csv', delimiter=',')
    X = df[['nodist_1', 'nodist_2', 'nodist_3', 'dist', 'types_same']]
    y = df[['target']]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    from sklearn.linear_model import LinearRegression

    #initiate linear regression model
    model = LinearRegression()
    model.fit(X.values, y.values)

    return model