"""
Version 1.02
- Created By Arif with help from
https://www.youtube.com/watch?v=J_LnPL3Qg70
"""
import pandas as pd
import math
from sklearn import linear_model

def FormatQual(column):
  column = column.replace("Ex", value="5")
  column = column.replace("Gd", value="4")
  column = column.replace("TA", value="3")
  column = column.replace("Fa", value="2")
  column = column.replace("Po", value="1")
  column = column.replace("NA", value="0")
  return column

def FormatSlope(column):
  column = column.replace("Gtl", value="3")
  column = column.replace("Mod", value="2")
  column = column.replace("Sev", value="1")
  return column

def FormatYesNo(column):
  column = column.replace("Y", value="1")
  column = column.replace("N", value="0")
  return column


ds = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/train.csv") #Reads the training data from the csv file and allocates it to a dataframe called ds
#### Following code changes qualatative columns into quantitative

ds.ExterQual = FormatQual(ds.ExterQual)
ds.LandSlope = FormatSlope(ds.LandSlope)
ds.CentralAir = FormatYesNo(ds.CentralAir)



Final_Dict = {'SalePrice': []} # Final dictionary to append to then be used to construct dataframe
#####Following makes median values so that it does not affect the prediction if there is a missing piece of information
MedianOverallQual = math.floor(ds.OverallQual.median())
MedianOverallCond = math.floor(ds.OverallCond.median())
MedianYearBuilt = math.floor(ds.YearBuilt.median())
MedianYrSold = math.floor(ds.YrSold.median())

####Following code replaces the N/A or null values
ds.OverallQual.fillna(MedianOverallQual)
ds.OverallCond.fillna(MedianOverallCond)
ds.YearBuilt.fillna(MedianYearBuilt)
ds.YrSold.fillna(MedianYrSold)


reg = linear_model.LinearRegression() #assigns the model to the variable linear regression "least squares model"

reg.fit(ds[['OverallQual','ExterQual','LandSlope','CentralAir','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces']], ds.SalePrice)

#print("the coefficients are ", reg.coef_)
#print("The y intercept is ", reg.intercept_)
#print(" the equation is :")
#print("y = {:.2f}x + {:.2f}z + {:.2f}t + {:.2f}I ".format(reg.coef_[0],reg.coef_[1],reg.coef_[2],reg.coef_[3]))
####Above code lets me view the equation of the line for debugging.
test_df = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/test.csv")

final_df = pd.DataFrame()

test_df.ExterQual = FormatQual(test_df.ExterQual)
test_df.LandSlope = FormatSlope(test_df.LandSlope)
test_df.CentralAir = FormatYesNo(test_df.CentralAir)

final_df['SalePrice'] = reg.predict(test_df[['OverallQual','ExterQual','LandSlope','CentralAir','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces']]).astype(int).tolist()
#above line creates the predictions of all the values within the test_dataframe(test_df)
final_df = final_df.set_index(test_df['Id'])
#Dataframes come with their own ID's that start from 0, our test set started from a custom figure so setting that
#Value from the Test_df was key to ensuring the submition was made correctly.
print(final_df.head())
final_df.to_csv(path_or_buf="submission.csv", index=True)
