import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing as PP
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


def aHash(img):

   # img=cv2.resize(img,(8,8),interpolation=cv2.INTER_CUBIC)

  #  gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=img
    s=0
    hash_str=''

    for i in range(8):
        for j in range(3):
            s=s+gray[i,j]

    avg=s/24

    for i in range(8):
        for j in range(3):
            if  gray[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str

def dHash(img):

    img=cv2.resize(img,(9,8),interpolation=cv2.INTER_CUBIC)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''

    for i in range(8):
        for j in range(8):
            if   gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str


data1=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S3.csv","rb"),delimiter=",",skiprows=0)
data2=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S4.csv","rb"),delimiter=",",skiprows=0)

data3=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Drink_Bottle\DB01S1.csv","rb"),delimiter=",",skiprows=0)
data4=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Drink_Bottle\DB01S2.csv","rb"),delimiter=",",skiprows=0)

data5=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S4.csv","rb"),delimiter=",",skiprows=0)
data6=np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S5.csv","rb"),delimiter=",",skiprows=0)

def STRTOHEX(str):
    data=str
    Hex=np.zeros(6)
    Hex[0] =eval(data[0])  * 8 +eval(data[1] ) * 4 + eval(data[2] ) * 2 + eval(data[3]  * 1)
    Hex[1] =eval(data[4])  * 8 +eval(data[5] ) * 4 + eval(data[6])  * 2 + eval(data[7]  * 1)
    Hex[2] =eval(data[8])  * 8 +eval(data[9] ) * 4 + eval(data[10]) * 2 + eval(data[11] * 1)
    Hex[3] =eval(data[12]) * 8 + eval(data[13]) *4 + eval(data[14]) * 2 + eval(data[15] * 1)
    Hex[4] =eval(data[16]) * 8 +eval(data[17]) * 4 + eval(data[18]) * 2 + eval(data[19] * 1)
    Hex[5] =eval(data[20]) * 8 +eval(data[21]) * 4 + eval(data[22]) * 2 + eval(data[23] * 1)
    return Hex

print(STRTOHEX(aHash(t(data1))))
print(STRTOHEX(aHash(t(data2))))

print(STRTOHEX(aHash(t(data3))))
print(STRTOHEX(aHash(t(data4))))

print(STRTOHEX(aHash(t(data5))))
print(STRTOHEX(aHash(t(data6))))

noram=PP.normalize(STRTOHEX(aHash(t(data4))))
print noram
stand=PP.scale(STRTOHEX(aHash(t(data4))))
print stand