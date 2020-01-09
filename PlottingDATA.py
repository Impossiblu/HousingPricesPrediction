import matplotlib.pyplot as mp
import pandas as pd


#This code uses Matplotlib, a library that can get numbers and other data from files and make graphs
#All you need to do is figure out how to make it so the pictures generated are saved as .jpegs or .pngs
#It uses the train.csv file so make sure thats in the same place when you run it
#PLus you might need to install pandas and matplotlib

df = pd.read_csv('train.csv')
data_top = list(df.columns)
data_top.remove('Id')
print(data_top)
#xstr = input("Please enter the column you wish to compare:")

for i in data_top: #for every variable in train.csv
    try:
        y = df['SalePrice'].values.tolist()#The y value on the graph is saleprice
        x = df[i].values.tolist() #the x value is selected as the variable in train.csv
        mp.scatter(x, y) #make a scatter with x and y
        mp.title('Variable scatter') #set the title as variable scatter
        mp.xlabel(i) #set the label as the title of x
        mp.ylabel('Sale_price') #y label is sale price
        mp.show() #show the graph
    except:
        print("The input ",i," isn't compatiable")