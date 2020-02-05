import pandas as pd
import numpy as np

quantVars = ['OverallQual','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces','YearRemodAdd','GarageCars','YrSold','GrLivArea','GarageArea','TotalBsmtSF'] # values are a number or null
qualVars = ['ExterQual','HeatingQC','KitchenQual','GarageQual','ExterCond'] # values are Ex Gd TA Fa Po or null
yesNoVars = ['CentralAir','PavedDrive'] # values are Y or N
yesNoNumberVars = [] # values are 0/null for N or number if Y # DISABLED AS IT HAD A NEGATIVE IMPACT ON RESULTS
otherVars = ['LandSlope'] # values dont follow a pattern and will be formatted seperatly

totalVars = quantVars + qualVars + yesNoVars + yesNoNumberVars + otherVars

def GetTotalVars():
    return totalVars

def FormatNulls(dataset):
    #List of columns where null values indicate 'None'
    colNone = ['Alley', 'MasVnrType', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC', 'Fence', 'MiscFeature', 'KitchenQual']
    
    #List of columns where nulls are replaced with the most common value
    colMostCommon = ['Electrical', 'MSZoning', 'Utilities', 'Exterior1st', 'Exterior2nd', 'Functional', 'SaleType']
    
    #List of columns where nulls are replaced with 0
    colZero = ['MasVnrArea', 'GarageYrBlt', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'GarageCars', 'GarageArea']
    
    for col in colNone:
        dataset[col] = dataset[col].fillna("None")
        
    for col in colMostCommon:
        dataset[col] = dataset[col].fillna(dataset[col].value_counts().idxmax())
        
    for col in colZero:
        dataset[col] = dataset[col].fillna(0)
    
    #Fill nulls based on LotFrontage values of houses in the same neighborhood
    for i in dataset.index:
        if (np.isnan(dataset.loc[i, 'LotFrontage'])):
            dataset.loc[i, 'LotFrontage'] = dataset.groupby('Neighborhood')['LotFrontage'].median()[dataset.loc[i, 'Neighborhood']]
    
    return dataset

def FormatQual(column):
    column = column.replace("Ex", value="5")
    column = column.replace("Gd", value="4")
    column = column.replace("TA", value="3")
    column = column.replace("Fa", value="2")
    column = column.replace("Po", value="1")
    column = column.replace("None", value="0")
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

def FormatData(dataset, removeAbnormals=False):
    dataset = FormatNulls(dataset)
    
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
    
    if removeAbnormals == True: #Remove houses with abnormal sale condiditon
        indexNames = dataset[dataset['SaleCondition'] == "Abnorml" ].index
        dataset.drop(indexNames, inplace=True)
        
        #shows the data set 
        display(dataset)
  
    return dataset
