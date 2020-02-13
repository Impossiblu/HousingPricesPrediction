"""
Version 1.45
- Created By Arif with help from
https://www.youtube.com/watch?v=J_LnPL3Qg70
https://www.kaggle.com/erick5/predicting-house-prices-with-machine-learning
https://www.youtube.com/watch?v=YKP31T5LIXQ

"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.pipeline import make_pipeline
from scipy.stats import norm
from warnings import simplefilter
from sklearn.preprocessing import scale
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn import ensemble

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


def PrepareFile(finalPrediction,IDs):
    print(type(finalPrediction))
    finalPrediction = np.expm1(finalPrediction)
    final_df = pd.DataFrame(finalPrediction)
    final_df.columns = ["SalePrice"]
    final_df = final_df.set_index(IDs)
    print(final_df.head())
    final_df.to_csv(path_or_buf="Submission.csv", index=True)

#def TrainModel(trainData):

DSTrain = pd.read_csv("train.csv") #Reads the training data from the csv file and allocates it to a dataframe called dsTrain
DSTest = pd.read_csv("test.csv") #Reads the testing data from the csv file and allocates it to the Dataframe called DSTEST

TrainID = DSTrain['Id'] #Save the IDS for both dataframes for the output later on
TestID = DSTest['Id']

DSTrain.drop("Id",axis = 1, inplace = True) # Drop the ID columns due to them being irrelevant
DSTest.drop("Id",axis = 1, inplace = True)

def NormalisationAnalysis(Df1):
    try:


        sns.distplot(Df1["SalePrice"], fit=norm)

        mean, stdDeviation = norm.fit(Df1["SalePrice"])
        print("Standard Deviation:{:.2f} Mean:{:.2f}".format(stdDeviation,mean))
        plt.legend(['Normal dist. {:.2f} and {:.2f}'.format(mean,stdDeviation)], loc='best')
        plt.ylabel("Frequency")
        plt.title("SalePrice distribution")

        fig = plt.figure()
        res = stats.probplot(Df1['SalePrice'], plot=plt)
        plt.show()

        print("Skewness: "+ Df1['SalePrice'].skew())# skew shows if more of the data is 'behind' the mean or infront of it with a negative or positive skew,
        # this can be seen with the bell curve being on a specific side
        print("Kurtosis: "+ Df1['SalePrice'].kurt()) # Kurtosis is a measurement of "tailedness" High kurtosis means lots of outliers and heavy tails and low means other
    except Exception as e:
        print("Analysis incorrect as :"+ e)
        pass


def Normalise(DF, Display = True):
    DF['SalePrice'] = np.log1p(DF["SalePrice"])
    if Display:
        sns.distplot(DF['SalePrice'] , fit=norm)

        # Get the fitted parameters used by the function
        mean, stdDeviation = norm.fit(DF["SalePrice"])

        print("Standard Deviation:{:.2f} Mean:{:.2f}".format(stdDeviation, mean))
        plt.legend(['Normal dist. {:.2f} and {:.2f}'.format(mean, stdDeviation)], loc='best')
        plt.ylabel('Frequency')
        plt.title('SalePrice distribution')

        fig = plt.figure()
        res = stats.probplot(DF['SalePrice'], plot=plt)
        plt.show()



        print("Skewness: {:.2f}".format(DF['SalePrice'].skew()))
        print("Kurtosis: {:.2f}".format(DF['SalePrice'].kurt()))
        print(DF.describe())
    return DF

def BuildModel(TrainDataset):

    TrainDataset = Normalise(TrainDataset, Display = False)
    regr = ensemble.BaggingRegressor(base_estimator=LinearRegression(), n_estimators=5, bootstrap=True)
    #ensemble bagging regressor using linear model, bootstrap entails that when values are taken they arent replaced
    regr.fit(TrainDataset[['OverallQual', 'OverallCond']], TrainDataset.SalePrice)
    return regr


PrepareFile(BuildModel(Normalise(DSTrain, Display=False)).predict(DSTest[['OverallQual', 'OverallCond']]), TestID)




