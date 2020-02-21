import pandas as pd
import math
from polynomialRegression import PolynomialRegression
from linearRegression import LinearRegression
from formatData import FormatData, FillMissingDummies, GetTotalVars

#Reads the training data from the csv file and allocates it to a dataframe called ds
ds = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/train.csv")
#Format train data with removal of rows with null values
ds = FormatData(ds, True)

#Import and format test data
test_df = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/test.csv")
#Format test data
test_df = FormatData(test_df)

#Ensures both datasets have the same columns
ds, test_df = FillMissingDummies(ds, test_df)

#Gets list of variables used to predict results
totalVars = GetTotalVars(test_df)

#Linear regression
linearReg_df = pd.DataFrame()

linearReg_df['SalePrice'] = LinearRegression(ds[totalVars], ds.SalePrice, test_df[totalVars]).astype(int).tolist()
#above line creates the predictions of all the values within the test_dataframe(test_df)

#Gives predictions correct Id and outputs results
linearReg_df = linearReg_df.set_index(test_df['Id'])
linearReg_df.to_csv(path_or_buf="submission.csv", index=True)

"""
#Polynomial regression
polyReg_df = pd.DataFrame()

polyDegree = 2  #Temp value - Have to decide what value to use properly. Higher values take exponentially more time and memory to process and do not work well with current data formatting

polyReg_df['SalePrice'] = PolynomialRegression(ds[totalVars], ds.SalePrice, polyDegree, test_df[totalVars]).astype(int).tolist()
#above line creates the predictions of all the values within the test_dataframe(test_df)
"""
