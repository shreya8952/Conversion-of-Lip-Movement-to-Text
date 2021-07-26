from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import itertools
from keras.utils import to_categorical
import h5py
import pickle

#preprocessing
df = pd.read_csv("combined_all3.csv")
df = df.drop(columns=["Unnamed: 0"]) #dropping the initial indexing column
df.iloc[:,90].replace("hello", 0,inplace=True)
df.iloc[:,90].replace("bye", 1,inplace=True)
df.iloc[:,90].replace("good", 2,inplace=True)
df.iloc[:,90].replace("day", 3,inplace=True)
df = df.astype(float)

data = np.array(df.iloc[:,90])

def encode(data):
    print('Shape of data (BEFORE encode): %s' % str(data.shape))
    encoded = to_categorical(data)
    print('Shape of data (AFTER  encode): %s\n' % str(encoded.shape))
    return encoded

encoded_data = encode(data)
coded = pd.DataFrame(encoded_data)
df = df.drop(columns=["90"])
coded.columns = ['1', '2', '3']
# print(coded)
df["90"] = coded["1"]
df["91"] = coded["2"]
df["92"] = coded["3"]


df = df.sample(frac=1)

df.to_csv("TOBETRAINED.csv")


names = df.columns[0:90]
scaler = MinMaxScaler() 
scalerfile = 'scaler.sav'
pickle.dump(scaler, open(scalerfile, 'wb'))
scaled_df = scaler.fit_transform(df.iloc[:,0:90]) 
scaled_df = pd.DataFrame(scaled_df, columns=names)



x=scaled_df.iloc[0:370,0:90] #.values.transpose()
y=df.iloc[0:370,90:93] #.values.transpose()
# print("here",y)
# xtest=scaled_df.iloc[300:370,0:90] #.values.transpose()
# ytest=df.iloc[300:370,90:93] #.values.transpose()
 


model = Sequential()

#2 hidden layers with the first input of 9
#one last hidden layer
model.add(Dense(12, input_dim=90, activation='relu')) #input_dim is the number of cols in the inputs
model.add(Dense(8, activation='relu'))
model.add(Dense(3, activation='softmax'))

# compile the keras model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#fit the keras model on the dataset
model.fit(x, y, epochs=30, batch_size=2)

model.save('my_model.h5')



# _, accuracy = model.evaluate(xtest, ytest)
# print('Accuracy: %.2f' % (accuracy*100))

# # evaluate the keras model
# #let us try working with a new test dataset
# test_df = pd.read_csv("testing.csv")
# test_df = test_df.drop(columns=["Unnamed: 0"]) #dropping the initial indexing column
# test_df.iloc[:,90].replace("hello", 0,inplace=True)
# test_df.iloc[:,90].replace("apple", 1,inplace=True)
# test_df.iloc[:,90].replace("banan", 2,inplace=True)
# test_df = test_df.astype(float)

# data = np.array(test_df.iloc[:,90])

# def encode(data):
#     print('Shape of data (BEFORE encode): %s' % str(data.shape))
#     encoded = to_categorical(data)
#     print('Shape of data (AFTER  encode): %s\n' % str(encoded.shape))
#     return encoded

# encoded_data = encode(data)
# coded = pd.DataFrame(encoded_data)
# test_df = test_df.drop(columns=["90"])
# coded.columns = ['1', '2', '3']
# # print(coded)
# test_df["90"] = coded["1"]
# test_df["91"] = coded["2"]
# test_df["92"] = coded["3"]


# test_df = test_df.sample(frac=1)

# test_df.to_csv("TOBETRAINED.csv")


# names = test_df.columns[0:90]
# scaler = MinMaxScaler() 
# scaled_df = scaler.fit_transform(test_df.iloc[:,0:90]) 
# scaled_df = pd.DataFrame(scaled_df, columns=names)

# x_test=scaled_df.iloc[0:9,0:89] #.values.transpose()
# y_test=test_df.iloc[0:9,90:93] #.values.transpose()



# _, accuracy = model.evaluate(xtest, ytest)
# print('Accuracy: %.2f' % (accuracy*100))
# values = model.predict_classes(x_test, verbose=1)
# print(y_test)
# print(values)




# _, accuracy = model.evaluate(xtest, ytest)
# print('Accuracy: %.2f' % (accuracy*100))


# values = model.predict_classes(xtest, verbose=1)
# print(ytest)
# print(values)



#k fold cross validation

# from sklearn.model_selection import KFold
 
# n_split=3
# X=scaled_df.iloc[:,0:89].values #.transpose()
# Y=df.iloc[:,90:93].values #.transpose()

# for train_index,test_index in KFold(n_split).split(X):

#     x_train,x_test=X[train_index],X[test_index]
#     y_train,y_test=Y[train_index],Y[test_index]

#     #   model=create_model()
#     model.fit(x_train, y_train,epochs=30,batch_size=2)

#     print('Model evaluation ')
#     _, accuracy = model.evaluate(x_test,y_test)
#     print('Accuracy: %.2f' % (accuracy*100))
