'''
csv 파일 dataframe으로 불러오고,
name에 'c68fe75ea'가 들어가는 것 중,
PixAcc가 sort에서 하위 query_num=30개만 가져오기
'''
import pandas as pd

query_num = 30
df = pd.read_csv('name_pixacc_train.csv')
df = df[df['name'].str.contains('c68fe75ea')].sort_values(by=['PixAcc'])['name'][:query_num].tolist()
print(df)
