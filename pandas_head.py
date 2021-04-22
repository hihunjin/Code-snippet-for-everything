'''
enlarge df.head(n)
'''

import pandas as pd
pd.set_option('display.max_rows', 500)
df = pd.read_csv('name_pixacc_train.csv')
df = df.sort_values(by=['PixAcc'])
df.head(100)
