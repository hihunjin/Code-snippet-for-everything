import matplotlib.pyplot as plt
import numpy as np

# array
np_array = np.array([0.8273090124,0.7899919152,0.7976203561,0.8474359512,0.6405683756,0.7574685216,0.04077241942,0.8054469228,0.8561310768,0.8297732472,0.8308554888,0.7532673478,0.7891752124,0.6220616698,0.8146234751,0.8059835434,0.5731907487,0.822198987,0.8079622388,0.8069797754,0.8214753866,0.810469985,0.6964287162,0.7906496525,0.8436586261,0.8355880976,0.8163226247,0.879838109,0.7803765535,0.8293119669])
np_array = np.sort(np_array)
ar = np.arange(len(np_array))

# plot
fig = plt.figure(figsize=(10,10))
plt.plot(ar,np_array,'.')
plt.yticks(np.arange(0,1,0.1))
plt.show()