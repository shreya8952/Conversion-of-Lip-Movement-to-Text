import numpy as np
from keras.utils import to_categorical
import pandas as pd


df = pd.read_csv("combined.csv")
df = df.drop(columns=["Unnamed: 0"]) #dropping the initial indexing column
df.iloc[:,90].replace("hello", 0,inplace=True)
df.iloc[:,90].replace("bye", 1,inplace=True)
df.iloc[:,90].replace("good", 2,inplace=True)
df.iloc[:,90].replace("day", 2,inplace=True)
df = df.astype(float)
data = np.array(df.iloc[:,90])
def encode(data):
    print('Shape of data (BEFORE encode): %s' % str(data.shape))
    encoded = to_categorical(data)
    print('Shape of data (AFTER  encode): %s\n' % str(encoded.shape))
    return encoded

encoded_data = encode(data)
coded = pd.DataFrame(encoded_data)
print(d)