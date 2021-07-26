#to combine and reshuffle the data sets

import pandas as pd

# df = pd.read_csv("combined_withshaals.csv")
df1 = pd.read_csv("hello.csv")
df2 = pd.read_csv("bye.csv")
df3 = pd.read_csv("good.csv")
df4 = pd.read_csv("day.csv")

results = ((df1.append(df2)).append(df3).append(df4)) #.append(df3)

results = results.drop(columns=["Unnamed: 0"]) #dropping the initial indexing column
results.to_csv("testing.csv")