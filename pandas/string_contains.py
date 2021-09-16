!wget https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv -O biostats.csv

import pandas as pd

df = pd.read_csv('biostats.csv')
df
# 	Name	"Sex"	"Age"	"Height (in)"	"Weight (lbs)"
# 0	Alex	"M"	41	74	170
# 1	Bert	"M"	42	68	166
# 2	Carl	"M"	32	70	155
# 3	Dave	"M"	39	72	167
# 4	Elly	"F"	30	66	124
# 5	Fran	"F"	33	66	115
# 6	Gwen	"F"	26	64	121
# 7	Hank	"M"	30	71	158
# 8	Ivan	"M"	53	72	175
# 9	Jake	"M"	32	69	143
# 10	Kate	"F"	47	69	139
# 11	Luke	"M"	34	72	163
# 12	Myra	"F"	23	62	98
# 13	Neil	"M"	36	75	160
# 14	Omar	"M"	38	70	145
# 15	Page	"F"	31	67	135
# 16	Quin	"M"	29	71	176
# 17	Ruth	"F"	28	65	131


df['Name'].str.contains('a')
# 0     False
# 1     False
# 2      True
# 3      True
# 4     False
# 5      True
# 6     False
# 7      True
# 8      True
# 9      True
# 10     True
# 11    False
# 12     True
# 13    False
# 14     True
# 15     True
# 16    False
# 17    False
# Name: Name, dtype: bool

df[df['Name'].str.contains('a')]
# 	Name	"Sex"	"Age"	"Height (in)"	"Weight (lbs)"
# 2	Carl	"M"	32	70	155
# 3	Dave	"M"	39	72	167
# 5	Fran	"F"	33	66	115
# 7	Hank	"M"	30	71	158
# 8	Ivan	"M"	53	72	175
# 9	Jake	"M"	32	69	143
# 10	Kate	"F"	47	69	139
# 12	Myra	"F"	23	62	98
# 14	Omar	"M"	38	70	145
# 15	Page	"F"	31	67	135
