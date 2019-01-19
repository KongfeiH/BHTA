import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def t(data):
    x=data.T[:,50]
    #x=x*(x>1.5)
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

test_matrix = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S0.csv","rb"),delimiter=",",skiprows=0)

img1=np.uint8(t(test_matrix))

plt.subplot(121)
plt.imshow(img1)
img = cv2.merge([img1])

sift=cv2.xfeatures2d.SIFT_create()
kp = sift.detect(img, None)  # 找到关键点

img = cv2.drawKeypoints(img, kp, img,flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,)  # 绘制关键点


height, width = img.shape[:2]
reSize1 = cv2.resize(img, (50*width,50*height), interpolation=cv2.INTER_CUBIC)
cv2.imshow("eqwe",reSize1)
#gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
plt.subplot(122)
plt.imshow(img)

plt.show()


cv2.waitKey(0)