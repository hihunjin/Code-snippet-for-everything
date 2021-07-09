import pandas as pd



# make a dataframe
df = pd.DataFrame(columns=['hi','im','david','.'])
df_len = len(df)
df.loc[df_len] = [3,1,2,0]


# All column names must be 'string' types
# df.columns = df.columns.astype(str)



# save
df.to_parquet('myfile.parquet', index=False)



# print
print(df)
#   hi im david  .
# 0  3  1     2  0


# read
df1 = pd.read_parquet('myfile.parquet')
df1
#   hi im david  .
# 0  3  1     2  0
