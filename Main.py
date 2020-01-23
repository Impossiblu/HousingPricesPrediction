import pandas as pd
import math
from polynomialRegression import PolynomialRegression
from linearRegression import LinearRegression
from formatData import FormatData, GetTotalVars

totalVars = GetTotalVars()  #Variables used when training models and predicting

#Reads the training data from the csv file and allocates it to a dataframe called ds
ds = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/train.csv")
#Format train data with removal of rows with null values
ds = FormatData(ds, True)

#Import and format test data
test_df = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/test.csv")
#Format test data
test_df = FormatData(test_df)


#Linear regression
linearReg_df = pd.DataFrame()

linearReg_df['SalePrice'] = LinearRegression(ds[totalVars], ds.SalePrice, test_df[totalVars]).astype(int).tolist()
#above line creates the predictions of all the values within the test_dataframe(test_df)
linearReg_df = linearReg_df.set_index(test_df['Id'])


#Polynomial regression
polyReg_df = pd.DataFrame()

polyDegree = 5  #Temp value - Have to decide what value to use properly. Higher values take exponentially more time to process

polyReg_df['SalePrice'] = PolynomialRegression(ds[totalVars], ds.SalePrice, polyDegree, test_df[totalVars]).astype(int).tolist()
#above line creates the predictions of all the values within the test_dataframe(test_df)
polyReg_df = polyReg_df.set_index(test_df['Id'])

#No output in this version as there are multiple sets of predictions that need to be combined somehow
