from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def predict(model,X_test,y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test,predictions)
    r2 = r2_score(y_test,predictions)
    return predictions,mse,r2