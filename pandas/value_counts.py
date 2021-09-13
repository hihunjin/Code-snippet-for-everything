# !wget https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv -O biostats.csv

import pandas as pd

df = pd.read_csv('biostats.csv')
df.columns
# Index(['Name', '     "Sex"', ' "Age"', ' "Height (in)"', ' "Weight (lbs)"'], dtype='object')

###### counts
df['     "Sex"'].value_counts()
#        "M"    11
#        "F"     7
# Name:      "Sex", dtype: int64
