import pandas as pd


# make a dataframe
df = pd.DataFrame([[1, 2], [3, 4]], columns = ["a", "b"])
print(df)
#    a  b
# 0  1  2
# 1  3  4


# append a list
to_append = [5, 6]
df_length = len(df)
df.loc[df_length] = to_append
print(df)
#    a  b
# 0  1  2
# 1  3  4
# 2  5  6
