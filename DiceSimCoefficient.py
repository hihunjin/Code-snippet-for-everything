'''
this is not validated
'''
import numpy as np
import pandas as pd


num_class = 4
pred = np.random.randint(0,num_class,(3,10,10))
grou = np.random.randint(0,num_class,(3,10,10))
df = pd.DataFrame(columns=['name']+[str(i) for i in range(num_class)]+['tp','fp','fn'])
for i in range(pred.shape[0]):
    d = {'name':i}
    d.update({str(i):False for i in range(num_class)})
    d.update({'tp':0, 'fp':0, 'fn': 0})
    for j in range(0,num_class):            ### if background is not computed, then 0 -> 1
        predT = pred[i]==j
        predF = np.logical_not(predT)
        gtT = grou[i]==j
        gtF = np.logical_not(gtT)
        tp = np.logical_and(predT,gtT).sum()
        fn = np.logical_and(predF,gtT).sum()
        fp = np.logical_and(gtF, predT).sum()
        d[str(j)]=2*tp / (2*tp+fp+fn)
        d['tp']+=tp
        d['fp']+=fp
        d['fn']+=fn
    
    df = df.append(d, ignore_index=True)
df.head()
