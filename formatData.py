import pandas as pd
import math

removeRowsWithNull = [] #any houses that have a null value for attributes in this array will be removed from calculations
#Placed here since I'm not sure how this is populated
#The only other place where this is refered to is reading values from it - Laurence

quantVars = ['OverallQual','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces','YearRemodAdd','GarageCars','YrSold','GrLivArea'] # values are a number or null
qualVars = ['ExterQual','HeatingQC','KitchenQual','GarageQual','ExterCond'] # values are Ex Gd TA Fa Po or null
yesNoVars = ['CentralAir','PavedDrive'] # values are Y or N
yesNoNumberVars = [] # values are 0/null for N or number if Y # DISABLED AS IT HAD A NEGATIVE IMPACT ON RESULTS
otherVars = ['LandSlope'] # values dont follow a pattern and will be formatted seperatly

totalVars = quantVars + qualVars + yesNoVars + yesNoNumberVars + otherVars

def GetTotalVars():
    return totalVars

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

def FormatData(dataset, removeNulls=False):
    for quant in quantVars: # fills all quant null vars with median
        dataset[quant] = dataset[quant].fillna(math.floor(dataset[quant].median()))
    
    for qual in qualVars: # changes all qual values to numbers and fills in nulls
        dataset[qual] = FormatQual(dataset[qual])
        dataset[qual] = dataset[qual].fillna('0')

    for yesNo in yesNoVars: # changes all yes no answers to 1's and 0's
        dataset[yesNo] = FormatYesNo(dataset[yesNo])
        dataset[yesNo] = dataset[yesNo].fillna('0')
    
    for yesNoNumber in yesNoNumberVars: # turns all number values to 1 if Y
        dataset[yesNoNumber] = dataset[yesNoNumber].fillna('0')
        dataset.loc[dataset[yesNoNumber] !='0', 'yesNoNumber'] = 1
    
    #other vars formatting
    dataset['LandSlope'] = FormatSlope(dataset['LandSlope'])
    
    if removeNulls == True: #Remove houses with null attributes or abnormal sale condiditon
        #removes all values with null values in certain columns
        for column in removeRowsWithNull:
            dataset = dataset[pd.notnull(dataset[column])]
        
        #Removes all houses with an abnormal sale condition
        indexNames = dataset[dataset['SaleCondition'] == "Abnorml" ].index
        dataset.drop(indexNames, inplace=True)
        
        #shows the data set 
        display(dataset)
  
    return dataset