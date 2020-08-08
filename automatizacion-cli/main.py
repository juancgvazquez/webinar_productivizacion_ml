from modules import preprocess,train,predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import glob
import sys
import pickle
import pandas as pd
import typer

app = typer.Typer()


@app.command()
def main(path: str):
    raw_files = []
    for files in glob.glob(path):
        raw_files.append(files)
    df = pd.read_csv(raw_files[0])
    X,y = preprocess.preprocess(df)
    model,X_test,y_test = train.train_randomforest(X,y)
    predictions = predict.predict(model,X_test)
    mse = mean_squared_error(y_test,predictions)
    r2 = r2_score(y_test,predictions)
    print("All Done")
    print("Metrics - MSE: {} R2: {}".format(mse,r2))
    preds = pd.DataFrame(predictions).reset_index().drop(columns='index')
    real = pd.DataFrame(y_test).reset_index().drop(columns='index')
    output = pd.concat([preds,real],axis=1,ignore_index=True)
    output.columns = ['preds','real']
    output.to_csv('output.csv',index=False)
    
@app.command()
def train_model(model_path:str,data_path:str,prov:str='Córdoba'):
    df=pd.read_csv(data_path)
    X,y = preprocess.preprocess(df,prov)
    model,X_test,y_test = train.train_randomforest(X,y)
    predictions = predict.predict(model,X_test)
    mse = mean_squared_error(y_test,predictions)
    r2 = r2_score(y_test,predictions)
    with open(model_path,'wb') as f:
        pickle.dump(model,f)
    print("All Done")
    print("Metrics - MSE: {} R2: {}".format(mse,r2))
    print("Model Saved in: %s" % model_path)


@app.command()
def predict_data(model_path:str,data_path:str,output_path:str):
    with open(model_path,'rb') as f:
        model = pickle.load(f)
    df = pd.read_csv(data_path)
    X,y = preprocess.preprocess(df)
    predictions = predict.predict(model,X)
    pd.DataFrame(predictions).to_csv(output_path,index=False)
    print("Predictions Done")
    print("Output file saved in: %s" % output_path)


if __name__ == '__main__':
    app()    