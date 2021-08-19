# plot with a sorted column
import random
import pandas as pd


# make a dataframe
df = pd.DataFrame(columns=['numbers'])
for i in range(100):
    df= df.append({'numbers':random.randint(0,300)}, ignore_index=True)
df


# sort
df1 = df.sort_values(by='numbers', ignore_index=True)     # ignore_index=True MUST!
# df1 = df.sort_values(by='numbers').reset_index()          # 왼쪽의 방법으로 되기도 함

# plot
df1.plot()
