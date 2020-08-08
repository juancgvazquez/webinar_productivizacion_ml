import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def train_randomforest(df2):
    X = df2[['surface_covered']]
    y = df2['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train,y_train)
    return model,X_test,y_test