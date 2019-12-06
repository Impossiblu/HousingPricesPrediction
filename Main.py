import pandas as pd
import tkinter as tk
import numpy as np
import matplotlib as mt
import math
from sklearn import linear_model

ds = pd.read_csv("train.csv")
f = []
#print(ds.SalePrice)
#print(ds.YearBuilt)

MedianOverallQual = math.floor(ds.OverallQual.median())
MedianOverallCond = math.floor(ds.OverallCond.median())
MedianYearBuilt = math.floor(ds.YearBuilt.median())
MedianYrSold = math.floor(ds.YrSold.median())
print(MedianOverallQual, MedianOverallCond,MedianYearBuilt)

ds.OverallQual.fillna(MedianOverallQual)
ds.OverallCond.fillna(MedianOverallCond)
ds.YearBuilt.fillna(MedianYearBuilt)
ds.YrSold.fillna(MedianYrSold)


reg = linear_model.LinearRegression()

reg.fit(ds[['OverallQual', 'OverallCond', 'YearBuilt', 'YrSold']], ds.SalePrice)

print("the coefficients are ", reg.coef_)
print("The y intercept is ", reg.intercept_)
print(" the equation is :")
print("y = {:.2f}x + {:.2f}z + {:.2f}t + {:.2f}I ".format(reg.coef_[0],reg.coef_[1],reg.coef_[2],reg.coef_[3]))

#x1 = ds['OverallQual'].values.reshape(1, -1)
#x2 = ds['OverallCond'].values.reshape(1, -1)
#x3 = ds['YearBuilt'].values.reshape(1, -1)





inputQual = float(input("Qual:"))
inputCond = float(input("Cond:"))
inputYearBuild = float(input("Year Built:"))
inputYearSold = float(input("Year Sold:"))

print(reg.predict([[inputQual, inputCond, inputYearBuild,inputYearSold]]))


