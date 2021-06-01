import pandas as pd

######## first row : columns
df = pd.read_csv('123.csv')
df


######## specifiy column names
colnames=['background', "Gallbladder", "Liver", "Pancreas", "Spleen", "Stomach"]
df = pd.read_csv('test.csv',names=colnames, header=None)
df
