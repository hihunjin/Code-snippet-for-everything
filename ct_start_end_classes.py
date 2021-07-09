import numpy as np
import pandas as pd


# define a dataframe
df = pd.DataFrame(columns=['case', 'num_slices', 'start', 'end', 'kidney_start','kidney_end', 'tumor_start', 'tumor_end', 'cyst_start','cyst_end'])


# define a row saving function
def load_csv(case_name, seg, df):
    
    new_row = [case_name]+[-1]*(len(df.columns)-1)
    new_row = dict(zip(df.columns, [case_name]+[-1]*(len(df.columns)-1)))
    for idx, array in enumerate(ex):
        if 1 in array:
            if new_row['kidney_start']==-1:
                new_row['kidney_start']=idx
            new_row['kidney_end']=idx
        if 2 in array:
            if new_row['tumor_start']==-1:
                new_row['tumor_start']=idx
            new_row['tumor_end']=idx
        if 3 in array:
            if new_row['cyst_start']==-1:
                new_row['cyst_start']=idx
            new_row['cyst_end']=idx
    new_row['start']=min(new_row['kidney_start'],new_row['tumor_start'],new_row['cyst_start'])
    new_row['end']=max(new_row['kidney_end'],new_row['tumor_end'],new_row['cyst_end'])
    new_row['num_slices'] = seg.shape[0]
    df = df.append(new_row, ignore_index=True)
    return df

# example array  
ex = np.random.randint(0,4,(10,2,2))
ex.max()


# save
df = load_csv('case_1',ex,df)

# print
print(df)
case	num_slices	start	end	kidney_start	kidney_end	tumor_start	tumor_end	cyst_start	cyst_end
0	case_1	10	0	9	1	9	0	9	0	9
