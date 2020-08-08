from modules import preprocess,train,predict
import glob
import sys
import pandas as pd

if __name__ == '__main__':
    raw_files = []
    path = '../data/raw/*.csv.gz'
    for files in glob.glob(path):
        raw_files.append(files)
    path=raw_files[0]
    df = pd.read_csv(path)
    df = preprocess.preprocess(df)
    model,X_test,y_test = train.train_randomforest(df)
    predictions,mse,r2 = predict.predict(model,X_test,y_test)
    print("All Done")
    print("Metrics - MSE: {} R2: {}".format(mse,r2))
    preds = pd.DataFrame(predictions).reset_index().drop(columns='index')
    real = pd.DataFrame(y_test).reset_index().drop(columns='index')
    output = pd.concat([preds,real],axis=1,ignore_index=True)
    output.columns = ['preds','real']
    output.to_csv('output.csv',index=False)
