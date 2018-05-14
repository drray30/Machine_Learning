import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

#Data split into training and testing set
data = pd.read_csv('train.csv')
data.dropna(axis=0,subset=['SalePrice'], inplace = True)
y = data.SalePrice
X = data.drop(['SalePrice'],axis=1).select_dtypes(exclude=['object'])

#creating validation set as well
train_X, test_X, train_y, test_y = train_test_split(X.as_matrix(),y.as_matrix(),test_size = 0.3)

#using imputer
my_imputer = Imputer()
train_X = my_imputer.fit_transform(train_X)
test_X = my_imputer.fit_transform(test_X)

#creating the XGboost mode for prediction of house prices

xgb_model = XGBRegressor()
xgb_model.fit(train_X, train_y, verbose=False)
predictions = xgb_model.predict(test_X)

#how well is your model doing: using Mean Absolute error
print("Mean Absolute Error : " + str(mean_absolute_error(predictions, test_y)))

#A look at parameter change to see if accuracy improves
xgb_model_2 = XGBRegressor(n_estimators=1000)
xgb_model_2.fit(train_X, train_y, early_stopping_rounds=5,
print("Mean Absolute Error : " + str(mean_absolute_error(predictions, test_y)))
