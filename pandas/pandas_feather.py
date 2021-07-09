import pandas as pd


# make a dataframe
df = pd.DataFrame(columns=['hi','im','david','.'])
df_len = len(df)
df.loc[df_len] = [3,1,2,0]



# print
print(df)
#   hi im david  .
# 0  3  1     2  0


# save
name = 'myfile.ftr'
df.to_feather(name)


# load
df1 = pd.read_feather(name)
print(df1)
#   hi im david  .
# 0  3  1     2  0


