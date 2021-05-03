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
grps = [4,1,1,1,1,1,2,4,2,4,2,2,2,3,3,4,3,3,3,4]
kfold = GroupKFold(n_splits=4).split(a, a, grps)
list(kfold)
