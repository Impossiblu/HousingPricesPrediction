import pandas as pd
import math
from sklearn import linear_model
from sklearn import ensemble


def FormatQual(column):
  column = column.replace("Ex", value="5")
  column = column.replace("Gd", value="4")
  column = column.replace("TA", value="3")
  column = column.replace("Fa", value="2")
  column = column.replace("Po", value="1")
  #column = column.replace("NA", value="0")
  #column = column.replace("nan", value="0")
  return column

def FormatSlope(column):
  column = column.replace("Gtl", value="3")
  column = column.replace("Mod", value="2")
  column = column.replace("Sev", value="1")
  return column

def FormatYesNo(column):
  column = column.replace("Y", value="1")
  column = column.replace("P", value="0.5")#partial
  column = column.replace("N", value="0")
  return column

ds = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/train.csv") #Reads the training data from the csv file and allocates it to a dataframe called ds


quantVars = ['OverallQual','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces','YearRemodAdd','GarageCars','YrSold','GrLivArea'] # values are a number or null
qualVars = ['ExterQual','HeatingQC','KitchenQual','GarageQual','ExterCond'] # values are Ex Gd TA Fa Po or null
yesNoVars = ['CentralAir','PavedDrive'] # values are Y or N
yesNoNumberVars = [] # values are 0/null for N or number if Y # DISABLED AS IT HAD A NEGATIVE IMPACT ON RESULTS
otherVars = ['LandSlope'] # values dont follow a pattern and will be formatted seperatly

removeRowsWithNull = [] #any houses that have a null value for attributes in this array will be removed from calculations

totalVars = quantVars + qualVars + yesNoVars + yesNoNumberVars + otherVars
totalVarString = "" #used for fit and predict function
for var in totalVars:# adding every var to a string of vars
  exec("totalVarString += \"'"+var+"',\"")
totalVarString = totalVarString[:-1] # removes last comma

def FormatData(dataset):
  for quant in quantVars: # fills all quant null vars with median
    exec(dataset+"." + quant + " = "+dataset+"." + quant + ".fillna(math.floor("+dataset+"." + quant + ".median()))")

  for qual in qualVars: # changes all qual values to numbers and fills in nulls
    exec(dataset+"."+qual+" = FormatQual("+dataset+"."+qual+")")
    exec(dataset+"."+qual+" = "+dataset+"."+qual+".fillna('0')")

  for yesNo in yesNoVars: # changes all yes no answers to 1's and 0's
    exec(dataset+"."+yesNo+" = FormatYesNo("+dataset+"."+yesNo+")")
    exec(dataset+"."+yesNo+" = "+dataset+"."+yesNo+".fillna('0')")

  for yesNoNumber in yesNoNumberVars: # turns all number values to 1 if Y
    exec(dataset+"."+yesNoNumber+" = "+dataset+"."+yesNoNumber+".fillna('0')")
    exec(dataset+".loc["+dataset+"."+yesNoNumber+" !='0', '"+yesNoNumber+"'] = 1")

  #other vars formatting
  exec(dataset+".LandSlope = FormatSlope("+dataset+".LandSlope)")

FormatData('ds')

#removes all values with null values in certain columns
for column in removeRowsWithNull:
  exec("ds = ds[pd.notnull(ds['" + column + "'])]")

#Removes all houses with an abnormal sale condition
indexNames = ds[ ds['SaleCondition'] == "Abnorml" ].index
ds.drop(indexNames , inplace=True)

#shows the data set
#display(ds)

Final_Dict = {'SalePrice': []} # Final dictionary to append to then be used to construct dataframe

regr = ensemble.BaggingRegressor(base_estimator=linear_model.LinearRegression(),n_estimators=5,bootstrap=True)

#Implements a new bagging technique that lets us use multiple linear regressions to combine the weak models into a better
#more accurate model, or thats what the wikipedia page says about baggings... so dont ask me


#reg = linear_model.LinearRegression() #assigns the model to the variable linear regression "least squares model"

exec("regr.fit(ds[["+totalVarString+"]], ds.SalePrice)")

#print("the coefficients are ", reg.coef_)
#print("The y intercept is ", reg.intercept_)
#print(" the equation is :")
#print("y = {:.2f}x + {:.2f}z + {:.2f}t + {:.2f}I ".format(reg.coef_[0],reg.coef_[1],reg.coef_[2],reg.coef_[3]))
####Above code lets me view the equation of the line for debugging.
test_df = pd.read_csv("https://raw.githubusercontent.com/Impossiblu/HousingPricesPrediction/master/test.csv")

final_df = pd.DataFrame()

FormatData('test_df')

exec("final_df['SalePrice'] = regr.predict(test_df[["+totalVarString+"]]).astype(int).tolist()")
#above line creates the predictions of all the values within the test_dataframe(test_df)
final_df = final_df.set_index(test_df['Id'])
#Dataframes come with their own ID's that start from 0, our test set started from a custom figure so setting that
#Value from the Test_df was key to ensuring the submition was made correctly.
print(final_df.head())
final_df.to_csv(path_or_buf="submission.csv", index=True)
