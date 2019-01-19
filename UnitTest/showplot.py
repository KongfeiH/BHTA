import sys
import numpy as np

#NP_LOADTXT = np.loadtxt(open("C:\Users\hekon\Desktop\\notook.csv", "rb"), delimiter=",", skiprows=0)
sys.path.append('../Helper/DataShow')
from  DataShow import DataShow as DS
show = DS()
test_matrix = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Book\BK01S0.csv","rb"),delimiter=",",skiprows=0)
test_matrix1 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Drink_Bottle\DB01S0.csv","rb"),delimiter=",",skiprows=0)
test_matrix2 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Glass_Cup\GC01S2.csv","rb"),delimiter=",",skiprows=0)
test_matrix3 = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\Ragdoll\RD01S3.csv","rb"),delimiter=",",skiprows=0)
none = np.loadtxt(open("E:\OneDrive\Python\BHand\Data\None\N01S2.csv","rb"),delimiter=",",skiprows=0)
show.PlotShow(test_matrix1.T,test_matrix1,test_matrix2,test_matrix3)