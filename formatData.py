import pandas as pd
import numpy as np

#The following lists contain all variables in the dataset, excluding Id and SalePrice
"""
quantVars = ['LotFrontage', 'LotArea', 'OverallQual', 'OverallCond', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'PoolArea', 'MiscVal', 'YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'MoSold', 'YrSold']
qualOrdinalVars = ['ExterQual', 'ExterCond', 'BsmtQual', 'BsmtCond', 'HeatingQC', 'KitchenQual', 'FireplaceQu', 'GarageQual', 'GarageCond', 'PoolQC', 'Functional', 'Fence', 'BsmtExposure']
qualNominalVars = ['MSSubClass', 'MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'BsmtFinType1', 'BsmtFinType2', 'Heating', 'CentralAir', 'Electrical', 'GarageType', 'GarageFinish', 'PavedDrive', 'MiscFeature', 'SaleType', 'SaleCondition']
"""
#These contain only the variables we were using previously
quantVars = ['OverallQual','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces','YearRemodAdd','GarageCars','YrSold','GrLivArea','GarageArea','TotalBsmtSF'] # values are a number or null
#Categorical values where categories have some kind of order (e.g. Excellent, Good, etc.)
qualOrdinalVars = ['ExterQual','HeatingQC','KitchenQual','GarageQual','ExterCond']
#Categorical values with no order
qualNominalVars = ['CentralAir','PavedDrive', 'LandSlope']

def GetTotalVars(dataset):
    dummyCols = []
    for col in dataset.columns:
        for i in qualNominalVars:
            if (i in col):
                dummyCols += [col]
    
    totalVars = quantVars + qualOrdinalVars + dummyCols
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

def FormatOrdinals(dataset, col):
    if (col == 'Functional'):
        return dataset[col].map({'Typ': 8, 'Min1': 7, 'Min2': 6, 'Mod': 5, 'Maj1': 4, 'Maj2': 3, 'Sev': 2, 'Sal':1 })
    elif (col == 'Fence'):
        return dataset[col].map({'GdPrv': 4, 'GdWo': 3, 'MnPrv': 2, 'MnWw': 1, 'None': 0})
    elif (col == "BsmtExposure"):
        return dataset[col].map({'Gd': 4, 'Av': 3, 'Mn': 2, 'No': 1, 'None': 0})
    else:
        return dataset[col].map({'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1, 'None': 0})

def FormatNominals(dataset, col):
    return pd.get_dummies(dataset, prefix=col, columns=[col])

def FillMissingDummies(train, test):
    colList = list(train.columns) + list(test.columns)
    colList.remove('SalePrice')
    
    for col in colList:
        if col not in list(train.columns):
            train[col]=0
            
        if col not in list(test.columns):
            test[col]=0
    
    return train, test

def FormatData(dataset, removeAbnormals=False):
    #Should always be done first
    dataset = FormatNulls(dataset)
    
    if removeAbnormals == True: #Remove houses with abnormal sale condiditon
        indexNames = dataset[dataset['SaleCondition'] == "Abnorml" ].index
        dataset.drop(indexNames, inplace=True)

    #Should always be done last
    for col in qualOrdinalVars:
        dataset[col] = FormatOrdinals(dataset, col)
        
    for col in qualNominalVars:
        dataset = FormatNominals(dataset, col)
        
    return dataset
