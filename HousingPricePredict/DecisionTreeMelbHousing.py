### Reading and getting data


import pandas as pd

melbourne_file_path = 'data\melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path)


# dropna drops missing values (think of na as "not available")
melbourne_data = melbourne_data.dropna(axis=0)

print(melbourne_data.columns)  # using .columns to check for the column name and reference table

melbourne_data.describe() # using .describe to check any missing values in each column

# dropna drops missing values (think of na as "not available")
melbourne_data = melbourne_data.dropna(axis=0)

# store the series of prices separately as melbourne_price_data.
melbourne_price_data = melbourne_data.Price


# the head command returns the top few lines of data.
print(melbourne_price_data.head())


### Selecting data

# selecting multiple columns
columns_of_interest = ['Landsize', 'BuildingArea']
two_columns_of_data = melbourne_data[columns_of_interest]

two_columns_of_data.describe()  # verifying we get the same columns we need

### Building model


y = melbourne_data.Price  # usually, we will make use of y as the target variable

# mannually selecting predictors is a traditional way but often effective if we have domain knowledge
melbourne_predictors = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea','YearBuilt', 'Lattitude', 'Longtitude']


X = melbourne_data[melbourne_predictors]  # by convention, we donate X as predictor


# often written in this format, the words in blue color are reserved words

from sklearn.tree import DecisionTreeRegressor

# Define model
melbourne_model = DecisionTreeRegressor()

# Fit model
melbourne_model.fit(X, y)

# making use of the first 5 records as predictors for prediction
print("Making predictions for the following 5 houses:")
print(X.head())
print("The predictions are")
print(melbourne_model.predict(X.head()))



### Model Validation on training dataset

from sklearn.metrics import mean_absolute_error  # using the MAE as evaluation metric

predicted_home_prices = melbourne_model.predict(X)

mean_absolute_error(y, predicted_home_prices)  # comparing the predicted y and the actual y


### test and train split to get test accuracy

from sklearn.model_selection import train_test_split # split dataset into training and validation

train_X, test_X, train_y, test_y = train_test_split(X, y,random_state = 0) # random_state =0 so that others can get the same set of training and testing dataset

# Define model
melbourne_model = DecisionTreeRegressor()

# Fit model using the training dataset
melbourne_model.fit(train_X, train_y)

# get predicted prices on test data

test_predictions = melbourne_model.predict(test_X)
print(mean_absolute_error(test_y, test_predictions))



### Fine tuning model for higher test accuracy

from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor


# self-defined function for capturing the comparison between different max_leaf_nodes

def get_mae(max_leaf_nodes, predictors_train, predictors_val, targ_train, targ_val):

    # fitting model with input max_leaf_nodes
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)

    # fitting the model with training dataset
    model.fit(predictors_train, targ_train)

    # making prediction with the test dataset
    preds_val = model.predict(predictors_val)

    # calculate and return the MAE
    mae = mean_absolute_error(targ_val, preds_val)
    return(mae)

# compare MAE with differing values of max_leaf_nodes

plot_mae = []

for max_leaf_nodes_counter in range(2,10):

    # get the mae for each iteration of for loop counter max_leaf_nodes_counter
    my_mae = get_mae(max_leaf_nodes_counter, train_X, train_X, train_y, test_y)

    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(max_leaf_nodes_counter, my_mae))

    plot_mae.append(my_mae)  

plot_mae = []
MLF = range(2,100)

for MLF_counter in range(2,100):
    my_mae = get_mae(MLF_counter,train_X,test_X,train_y,test_y)
    # print("Max Leaf nodes : %d \t\t Mean Absolute Error:  %d" %(MLF_counter,my_mae))
    plot_mae.append(my_mae)

import matplotlib.pyplot as plt

plt.plot(MLF,plot_mae)