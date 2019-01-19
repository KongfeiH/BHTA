from scipy.fftpack  import rfft
from scipy.fftpack import fftshift
from scipy.signal import medfilt,filtfilt,wiener,detrend
from sklearn.decomposition import PCA
from scipy import  signal
import numpy as np
import matplotlib.pyplot as plt
data=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Drink_Bottle\DB01S0.csv","rb"),delimiter=",",skiprows=0)
data1=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Drink_Bottle\DB01S1.csv","rb"),delimiter=",",skiprows=0)
data2=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Drink_Bottle\DB01S2.csv","rb"),delimiter=",",skiprows=0)


data3=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S0.csv","rb"),delimiter=",",skiprows=0)
data4=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S1.csv","rb"),delimiter=",",skiprows=0)
data5=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S2.csv","rb"),delimiter=",",skiprows=0)


data6=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S0.csv","rb"),delimiter=",",skiprows=0)
data7=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S1.csv","rb"),delimiter=",",skiprows=0)
data8=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S2.csv","rb"),delimiter=",",skiprows=0)



#plt.plot(data.T[:,50])
#plt.show()
data_fft =fftshift(rfft(data.T))

plt.subplot(321)
plt.plot(data)
plt.grid()
plt.subplot(322)
plt.plot(data1)
plt.grid()


plt.subplot(323)
plt.plot(data3)
plt.grid()
plt.subplot(324)
plt.plot(data4)
plt.grid()


plt.subplot(325)
plt.plot(data6)
plt.grid()
plt.subplot(326)
plt.plot(data7)
plt.grid()

plt.show()
'''

x=data8.T[:,50]
DA=np.hstack((x,x[24:48],x[72:]))
pca=PCA(n_components=1)
pca.fit(DA.reshape(2, 72))
X_new = pca.transform(DA.reshape(2,-1))
print(X_new)
plt.scatter(X_new[0], X_new[1],marker='o')
plt.show()
'''
'''
def t(data):
    x=data.T[:,50]
    x=x*(x>1.5)
    dataTest = np.array([x[0:3],
                        x[3:6],
                        x[6:9],
                        x[9:12],
                        x[12:15],
                        x[15:18],
                        x[18:21],
                        x[21:24]])
    dataTest1 = np.array([x[24:27],
                         x[27:30],
                         x[30:33],
                         x[33:36],
                         x[36:39],
                         x[39:42],
                         x[42:45],
                         x[45:48]])
    dataTest2 = np.array([x[48:51],
                         x[51:54],
                         x[54:57],
                         x[57:60],
                         x[60:63],
                         x[63:66],
                         x[66:69],
                         x[69:72]])
    x1 = x[72:77]

    x1=np.insert(x1,0,0)
    x1=np.append(x1,values=0)

    y1 =x[91:96]
    y1=np.insert(y1,0,0)
    y1=np.append(y1,values=0)
    dataTest3 = np.array([x1,
                         x[77:84],
                         x[84:91],
                         y1])
   # fig1=plt.figure(figname)
    plt.subplot(221)
    plt.imshow(dataTest)
    plt.subplot(222)
    plt.imshow(dataTest1)
    plt.subplot(223)
    plt.imshow(dataTest2)
    plt.subplot(224)
    plt.imshow(dataTest3)
    plt.show()

t(data)
t(data1)
t(data2)
t(data3)
t(data4)
t(data5)
t(data6)
t(data7)
t(data8)

'''
