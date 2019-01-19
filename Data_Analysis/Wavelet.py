import numpy as np
import pywt
import matplotlib.pyplot as plt

data=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S7.csv","rb"),delimiter=",",skiprows=0)
(ca,cd)=pywt.dwt(data[:,:   ],'db2')
plt.subplot(311)
plt.plot(ca)
plt.subplot(312)
plt.plot(cd)
plt.subplot(313)
plt.plot(data[:,7])
plt.show()