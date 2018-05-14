#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:15:22 2018

@author: deepa
"""

#Code for opening files online

#code for making sure http files are open on mac without context errors
def httpopen():
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    return

def summary_stats(dataframe1):
    print("The shape of dataframe is : %d rows and %d columns" %(df.shape[0],df.shape[1]))
    
#calling the files for opening
httpopen()

#importing all the utilities for data manipulation and plotting
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Machine learning imports
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


#reading the file into dataframe from an url
df=pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/semeion/semeion.data",
               sep=" ", header=None)
summary_stats(df.shape)

##plot the image to see if the first few digits look ok
#imagshow=np.reshape(df.loc[0,0:255],(16,16))
#plt.imshow(imagshow)

#last column dropped due to NA values
df=df.drop(columns=[266])

#splitting into training and testing datasets , random state only for reproducibility of results
from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size=0.5, random_state=10)
X_train=train.iloc[:,0:256]
X_test=test.iloc[:,0:256]
y_train=train.iloc[:,256:]
y_test=test.iloc[:,256:]

#Specifying the input classes and the shape of each data point
input_shape=(16,16,1)
num_classes=10

#reshaping the data before feeding into the model
X_train=np.array(X_train.values).reshape(-1,16,16,1)
X_test=np.array(X_test.values).reshape(-1,16,16,1)

##defining the model
model=Sequential()
model.add(Conv2D(filters=16, kernel_size=(4,4), activation='relu',input_shape=input_shape,
                 padding="same"))
model.add(Conv2D(32, (5, 5), activation='relu',input_shape=input_shape))

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))


#making the final model, with trials for different optimizer functions
##Adagrad,Adadelta, RMSprop- as optimizer functions
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adagrad(), 
              metrics=['accuracy'])
#fitting the data to the model
history=model.fit(X_train, y_train,
          batch_size=75,
          epochs=25,
          verbose=1,
          validation_data=(X_test, y_test),validation_split=0.5)

#scoring the data on the test dataset
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#converting epoch to np array so that it can be plotted
epochs=np.arange(0,25)
#plt.style.use('ggplot')

#getting values to plot the loss curve as well as accuracy curve
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
fig, axes = plt.subplots(1,2,figsize=(16,8))

axes[0].plot(epochs, acc, 'bo', label='Training acc')
axes[0].plot(epochs, val_acc, 'b', label='Validation acc')
axes[0].set_title('Training and validation accuracy')
axes[0].legend()
axes[1].plot(epochs, loss, 'bo', label='Training loss')
axes[1].plot(epochs, val_loss, 'b', label='Validation loss')
axes[1].set_title('Training and validation loss')
axes[1].legend()

#how would we predict the digits with some input
#model.predict_classes(X_test[0:1])
#this would return the class the prediction falls in

#one could save this model for future prediction
model.save('semianmodel.h5')  # creates a HDF5 file 'of the model
del model  # deletes the existing model


#you could load the model at a later date  and use it for prediction
from keras.models import load_model
semmodel=load_model("semianmodel.h5")
semmodel.predict_classes(X_test[0:1])