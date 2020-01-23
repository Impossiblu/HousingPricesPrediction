from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
    
def PolynomialRegression(trainData, targetValues, degree, predictData, returnReg=False):
    #Define linear regression model
    reg = linear_model.LinearRegression()
    
    #Define polynomial features
    polynomial_features = PolynomialFeatures(degree=degree)
    
    #Transform train data
    polyTrainData = polynomial_features.fit_transform(trainData)
    
    #Transform test data
    polyPredictData = polynomial_features.fit_transform(predictData)
    
    #Fit train data to model using target values
    reg.fit(polyTrainData, targetValues)
    
    #Return predictions from test data
    if (returnReg == False):
        return reg.predict(polyPredictData)
    else:
        return reg