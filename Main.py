import pandas as pd
import numpy as np
from formatData import FormatData, FillMissingDummies, GetTotalVars
from modelling import Predict

import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn

def rmsle(real, predicted):
    sum=0.0
    for x in range(len(predicted)):
        p = np.log(predicted[x]+1)
        r = np.log(real[x]+1)
        sum = sum + (p - r)**2
    return (sum/len(predicted))**0.5

def OutputPrediction(prediction, ids):
    outDf = pd.DataFrame()
    
    outDf['SalePrice'] = prediction.astype(int).tolist()
    
    outDf = outDf.set_index(ids)
    
    outDf.to_csv('submission.csv')
    
    linr = rmsle(pd.read_csv("train.csv")['SalePrice'].values, outDf['SalePrice'].values)
    print("score: " + str(linr))

def MainPredict(trainFileName, testFileName):
    train = pd.read_csv(trainFileName)
    test = pd.read_csv(testFileName)
    
    train = FormatData(train, True)
    
    test = FormatData(test)
    
    train, test = FillMissingDummies(train, test)
    
    totalVars = GetTotalVars(test)
    
    OutputPrediction(Predict(train[totalVars], train.SalePrice, test[totalVars]), test['Id'])
 
#Used only when running from this file, comment out when running from gui.py
#MainPredict("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/train.csv", "https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/test.csv")
