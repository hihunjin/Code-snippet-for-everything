img = ['123123','5365346','245235','3333']
msk = ['m123123','m5365346','m245235', 'm3333']

double = ['23']
ignore = ['36']

new_img, new_msk = [], []
def check(li, idx):
    for e in li:
        if e in idx:
            return True
    
    return False

assert len(img)==len(msk)
for i,j in zip(img,msk):
    if check(double,i):
        new_img.extend([i]*2)
        new_msk.extend([j]*2)
    elif check(ignore,i):
        continue
    else:
        new_img.append(i)
        new_msk.append(j)
        
print(new_img)
print(new_msk)
