# %%capture
# !wget https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv -O biostats.csv

import pandas as pd
df = pd.read_csv('biostats.csv')
df = df.set_index("Name")

print(df.iloc[0])
