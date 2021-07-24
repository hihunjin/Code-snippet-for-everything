from sklearn.model_selection import KFold, GroupKFold, StratifiedKFold

'''
kfold
'''

a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
b = KFold(n_splits=5,
              random_state=1,
              shuffle=True).split(a)
list(b)

'''
group kfold
'''
grps = [3,1,1,1,1,1,2,3,2,3,2,2,2,3,3,3,3,3,3,3]
gkfold = GroupKFold(n_splits=2).split(a, a, grps)
list(gkfold)

'''
Stratified KFold
'''
grps = [3,1,1,1,1,1,2,3,2,3,2,2,2,3,3,3,3,3,3,3]
skfold = StratifiedKFold(n_splits=6, random_state=1,
              shuffle=True).split(a, grps)
list(skfold)
# [(array([ 0,  1,  3,  4,  5,  6,  7,  9, 10, 11, 12, 13, 15, 17, 18, 19]),
#   array([ 2,  8, 14, 16])),
#  (array([ 1,  2,  4,  5,  6,  7,  8,  9, 11, 12, 13, 14, 16, 17, 18, 19]),
#   array([ 0,  3, 10, 15])),
#  (array([ 0,  1,  2,  3,  5,  6,  7,  8,  9, 10, 11, 12, 14, 15, 16, 17, 18]),
#   array([ 4, 13, 19])),
#  (array([ 0,  1,  2,  3,  4,  5,  6,  7,  8, 10, 12, 13, 14, 15, 16, 18, 19]),
#   array([ 9, 11, 17])),
#  (array([ 0,  2,  3,  4,  5,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 19]),
#   array([ 1,  6, 18])),
#  (array([ 0,  1,  2,  3,  4,  6,  8,  9, 10, 11, 13, 14, 15, 16, 17, 18, 19]),
#   array([ 5,  7, 12]))]
