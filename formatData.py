import pandas as pd
import numpy as np
from scipy.stats import skew
from scipy.special import boxcox1p

#The following lists contain all variables in the dataset, excluding Id and SalePrice
#Unsure of how to represent, all except 'BsmtExposure', which is placed in ordinal, placed in quant: 
#'YearBuilt', 'YearRemodAdd','GarageYrBlt', 'MoSold', 'YrSold', 'BsmtExposure'
"""
quantVars = ['LotFrontage', 'LotArea', 'OverallQual', 'OverallCond', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'PoolArea', 'MiscVal', 'YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'MoSold', 'YrSold', 'TotalSF']
qualOrdinalVars = ['ExterQual', 'ExterCond', 'BsmtQual', 'BsmtCond', 'HeatingQC', 'KitchenQual', 'FireplaceQu', 'GarageQual', 'GarageCond', 'PoolQC', 'Functional', 'Fence', 'BsmtExposure']
qualNominalVars = ['MSSubClass', 'MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'BsmtFinType1', 'BsmtFinType2', 'Heating', 'CentralAir', 'Electrical', 'GarageType', 'GarageFinish', 'PavedDrive', 'MiscFeature', 'SaleType', 'SaleCondition']
"""
#These contain only the variables we were using previously
#Values are a number
quantVars = ['OverallQual','FullBath','BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces','GarageCars','GrLivArea','GarageArea','TotalBsmtSF','TotalSF'] 
#Categorical values where categories have some kind of order (e.g. Excellent, Good, etc.)
qualOrdinalVars = ['ExterQual','HeatingQC','KitchenQual','GarageQual','ExterCond']
#Categorical values with no order
qualNominalVars = ['CentralAir','PavedDrive', 'LandSlope','YrSold','YearRemodAdd']

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

def RemoveOutliers(train):
    #GrLivArea
    train = train.drop(train[(train['GrLivArea']>4000) & (train['SalePrice']<300000)].index).reset_index(drop=True)
    """
    #GarageCars
    train = train.drop(train[(train['GarageCars']>3) & (train['SalePrice']<300000)].index).reset_index(drop=True)
    
    #GarageArea
    train = train.drop(train[(train['GarageArea']>1000) & (train['SalePrice']<300000)].index).reset_index(drop=True)
    
    #MasVnrArea
    train = train.drop(train[(train['MasVnrArea']>1500) & (train['SalePrice']<300000)].index).reset_index(drop=True)
    
    #LotFrontage
    train = train.drop(train[(train['LotFrontage']>300) & (train['SalePrice']<300000)].index).reset_index(drop=True)
    
    #OpenPorchSF
    train = train.drop(train[(train['OpenPorchSF']>500) & (train['SalePrice']<100000)].index).reset_index(drop=True)
    
    #LotArea
    train = train.drop(train[(train['LotArea']>150000) & (train['SalePrice']<400000)].index).reset_index(drop=True)
    
    #ScreenPorch
    train = train.drop(train[(train['ScreenPorch']>350) & (train['SalePrice']<200000)].index).reset_index(drop=True)
    
    #PoolArea
    train = train.drop(train[(train['PoolArea']>400) & (train['SalePrice']>700000)].index).reset_index(drop=True)
    
    #MoSold
    train = train.drop(train[(train['MoSold']>0.0) & (train['SalePrice']>700000)].index).reset_index(drop=True)
    
    #3SsnPorch
    train = train.drop(train[(train['SalePrice']>360000)].index).reset_index(drop=True)
    
    #LandContour
    train = train.drop(train[(train['LandContour']=='Bnk') & (train['SalePrice']<200000)].index).reset_index(drop=True)
    
    #EnclosedPorch
    train = train.drop(train[(train['EnclosedPorch']>500) & (train['SalePrice']>200000)].index).reset_index(drop=True)
    train = train.drop(train[(train['EnclosedPorch']>100) & (train['SalePrice']>150000)].index).reset_index(drop=True)
    
    #MiscVal
    train = train.drop(train[(train['MiscVal']>2500) & (train['SalePrice']<100000)].index).reset_index(drop=True)
    
    #YrSold
    train = train.drop(train[(train['YrSold']==2006) & (train['SalePrice']<100000)].index).reset_index(drop=True)
    train = train.drop(train[(train['YrSold']==2007) & (train['SalePrice']<100000)].index).reset_index(drop=True)
    """
    return train

def ModifiedVariables(dataset):
    #TotalSF
    dataset['TotalSF'] = dataset['TotalBsmtSF'] + dataset['1stFlrSF'] + dataset['2ndFlrSF']
        
    return dataset

def Skew(dataset):
    skewed_feats = dataset[quantVars].apply(lambda x: skew(x.dropna())).sort_values(ascending=True)
    skewness = pd.DataFrame({'Skew': skewed_feats})
    
    skewness = skewness[abs(skewness) > 0.75]
    skewed_features = skewness.index
    lam = 0.15
    for feat in skewed_features:
        dataset[feat] = boxcox1p(dataset[feat], lam)
        
    return dataset

def FormatData(dataset, trainSet=False):
    #Should always be done first
    dataset = FormatNulls(dataset)
    
    dataset = ModifiedVariables(dataset)
    
    if trainSet == True: #Remove houses with abnormal sale condiditon
        indexNames = dataset[dataset['SaleCondition'] == "Abnorml"].index
        dataset.drop(indexNames, inplace=True)
        
        dataset = RemoveOutliers(dataset)
        
        #Normalization
        dataset['SalePrice'] = np.log1p(dataset['SalePrice'])
        
    dataset = Skew(dataset)
    

    #Should always be done last
    for col in qualOrdinalVars:
        dataset[col] = FormatOrdinals(dataset, col)
        
    for col in qualNominalVars:
        dataset = FormatNominals(dataset, col)
        
    return dataset

