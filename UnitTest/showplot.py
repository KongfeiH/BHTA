import sys
import numpy as np

#NP_LOADTXT = np.loadtxt(open("C:\Users\hekon\Desktop\\notook.csv", "rb"), delimiter=",", skiprows=0)
sys.path.append('../Helper/DataShow')
from  DataShow import DataShow as DS
show = DS()
test_matrix = np.loadtxt(open("C:\Users\hekon\Desktop\zhitong S.csv","rb"),delimiter=",",skiprows=0)
test_matrix1 = np.loadtxt(open("C:\Users\hekon\Desktop\kongs.csv","rb"),delimiter=",",skiprows=0)
show.PlotShow(test_matrix,test_matrix1)