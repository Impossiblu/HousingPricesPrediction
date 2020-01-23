from sklearn import linear_model

def LinearRegression(trainData, targetValues, predictData, returnReg=False):
    #Define linear regression model
    reg = linear_model.LinearRegression()
    
    #Fit train data to model using trget values
    reg.fit(trainData, targetValues)
    
    #Return predicted values from test data
    if (returnReg == False):
        return reg.predict(predictData)
    else:
        return reg