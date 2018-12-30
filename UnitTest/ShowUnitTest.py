import sys
import numpy as np

#NP_LOADTXT = np.loadtxt(open("C:\Users\hekon\Desktop\\notook.csv", "rb"), delimiter=",", skiprows=0)
sys.path.append('../Helper/DataShow')
from  DataShow import DataShow as DS

show = DS()
test_matrix = np.loadtxt(open("C:\Users\hekon\Desktop\cjz.csv","rb"),delimiter=",",skiprows=0)
test_matrix1 = np.loadtxt(open("C:\Users\hekon\Desktop\cjz1.csv","rb"),delimiter=",",skiprows=0)
test_matrix2 = np.loadtxt(open("C:\Users\hekon\Desktop\Fabric.csv","rb"),delimiter=",",skiprows=0)
test_matrix3 = np.loadtxt(open("C:\Users\hekon\Desktop\Fabric1.csv","rb"),delimiter=",",skiprows=0)
test_matrix4 = np.loadtxt(open("C:\Users\hekon\Desktop\zhitong.csv","rb"),delimiter=",",skiprows=0)
test_matrix5 = np.loadtxt(open("C:\Users\hekon\Desktop\zhitong1.csv","rb"),delimiter=",",skiprows=0)
kong = np.loadtxt(open("C:\Users\hekon\Desktop\kong.csv","rb"),delimiter=",",skiprows=0)

#test_matrix5 = #NP_LOADTXT
#show.ImgineShow(np.arange(600).reshape(20,30))
show.ImgineShow(test_matrix-kong,test_matrix1-kong,test_matrix2-kong,test_matrix3-kong,test_matrix4-kong,test_matrix5-kong,n=6)