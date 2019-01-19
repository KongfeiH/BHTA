import sys
import numpy as np

#NP_LOADTXT = np.loadtxt(open("C:\Users\hekon\Desktop\\notook.csv", "rb"), delimiter=",", skiprows=0)
sys.path.append('../Helper/DataShow')
from  DataShow import DataShow as DS

show = DS()
test_matrix  = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S0.csv","rb"),delimiter=",",skiprows=0)
test_matrix1 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S1.csv","rb"),delimiter=",",skiprows=0)
test_matrix2 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S2.csv","rb"),delimiter=",",skiprows=0)
test_matrix3 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S3.csv","rb"),delimiter=",",skiprows=0)
test_matrix4 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S4.csv","rb"),delimiter=",",skiprows=0)
test_matrix5 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\None\N01S1.csv","rb"),delimiter=",",skiprows=0)

#test_matrix5 = #NP_LOADTXT
#show.ImgineShow(np.arange(600).reshape(20,30))
show.ImgineShow(test_matrix,test_matrix1,test_matrix2,test_matrix3,test_matrix4,test_matrix5,n=6)