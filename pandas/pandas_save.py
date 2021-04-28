import pandas as pd
a_dataframe = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
a_dataframe.to_csv('123.csv', index=False)
