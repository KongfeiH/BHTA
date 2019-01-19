import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
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
    return dataTest
data1=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S3.csv","rb"),delimiter=",",skiprows=0)
data2=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S4.csv","rb"),delimiter=",",skiprows=0)

data3=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S3.csv","rb"),delimiter=",",skiprows=0)
data4=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S4.csv","rb"),delimiter=",",skiprows=0)


tsne = TSNE(n_components=2)
tsne.fit_transform(t(data1))
print(tsne.embedding_)

tsne1 = TSNE(n_components=2)
tsne1.fit_transform(t(data2))
print(tsne1.embedding_)

tsne2 = TSNE(n_components=2)
tsne2.fit_transform(t(data3))
print(tsne2.embedding_)

tsne3 = TSNE(n_components=2)
tsne3.fit_transform(t(data4))
print(tsne3.embedding_)






plt.subplot(221)
plt.imshow(t(data1),cmap=plt.cm.gray_r)
plt.subplot(222)
plt.imshow(t(data2),cmap=plt.cm.gray_r)
plt.subplot(223)
plt.imshow(t(data3),cmap=plt.cm.gray_r)
plt.subplot(224)
plt.imshow(t(data4),cmap=plt.cm.gray_r)
plt.show()