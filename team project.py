import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#important library for linear regration
from sklearn.linear_model import LinearRegression



data = pd.read_csv('train.csv', index_col=0)

#function that creates and prints graphs
def FormatColumn(column):
  column = column.replace("Ex", 5)
  column = column.replace("Gd", 4)
  column = column.replace("TA", 3)
  column = column.replace("Fa", 2)
  column = column.replace("Po", 1)
  column = column.replace("NA", 0)
  column = column.replace('Gtl', 3)
  column = column.replace('Mod', 2)
  column = column.replace('Sev', 1)
  return column

#polynomia regration:   
def graphp(parameter1):
    print("")
    print ("this is the graph for:" ,parameter1)

    x=data[parameter1]
    y=data['SalePrice']
    
    plt.scatter(x,y)
    
    z= np.polyfit(x,y, 1)
    f = np.poly1d(z)
    
    plt.plot(x,f(x))
    plt.show()
    
    
    
    
    
    
def graphl(parameter1):
    
    print(" ")
    print ("this is the graph for linear regration:" ,parameter1)
    
    X=data[parameter1].values.reshape(1, -1)
    Y=data['SalePrice'].values.reshape(1, -1)
    
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.show()

   
    
 
    

#main
    
#calls to sort out the data into a readable form
    
data['ExterQual'] = FormatColumn(data['ExterQual'])
data['LandSlope'] = FormatColumn(data['LandSlope'])
data['KitchenQual'] = FormatColumn(data['KitchenQual'])


#calls for polynomia regration:

graphp('ExterQual')

graphp('LandSlope')

graphp('OverallQual')

graphp('BedroomAbvGr')

graphp('Fireplaces')

graphp('KitchenQual')

graphp('TotRmsAbvGrd')



#calls graphs for lenear regration 

graphl('ExterQual')

graphl('LandSlope')


##maybe i do not understand the concept but it looks like the polynomial r.
##is the same as the linear regration graph 




