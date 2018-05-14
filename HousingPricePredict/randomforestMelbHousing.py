### Reading and getting data


import pandas as pd

melbourne_file_path = '../input/melbourne-housing-snapshot/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path)

### Building model

# setting the predictor and the target variable

y = melbourne_data.Price  # usually, we will make use of y as the target variable

# mannually selecting predictors is a traditional way but often effective if we have domain knowledge
melbourne_predictors = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea','YearBuilt', 'Lattitude', 'Longtitude']

X = melbourne_data[melbourne_predictors]  # by convention, we donate X as predictor

from sklearn.model_selection import train_test_split # split dataset into training and validation

train_X, test_X, train_y, test_y = train_test_split(X, y,random_state = 0) # random_state =0 so that others can get the same set of training and testing dataset


# random forest is under ensemble method

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# define, fit, predict and evaluation in simple four lines of code
rf_model = RandomForestRegressor()
rf_model.fit(train_X, train_y)
melb_preds = rf_model.predict(test_X)
print(mean_absolute_error(test_y, melb_preds))



def get_mae_rf(num_est, predictors_train, predictors_val, targ_train, targ_val):

    # fitting model with input max_leaf_nodes
    model = RandomForestRegressor(n_estimators=num_est, random_state=0)

    # fitting the model with training dataset
    model.fit(predictors_train, targ_train)

    # making prediction with the test dataset
    preds_val = model.predict(predictors_val)

    # calculate and return the MAE
    mae = mean_absolute_error(targ_val, preds_val)
    return(mae)

plot_mae = []
estimator = range(2,10)


for num_est  in range(2,100):
    my_mae = get_mae_rf(num_est,train_X,test_X,train_y,test_y)
    #print("Max Leaf nodes : %d \t\t Mean Absolute Error:  %d" %(num_est,my_mae))
    plot_mae.append(my_mae)

import matplotlib.pyplot as plt

plt.plot(estimator,plot_mae)
