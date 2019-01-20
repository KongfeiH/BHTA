import sys
import numpy as np

#NP_LOADTXT = np.loadtxt(open("C:\Users\hekon\Desktop\\notook.csv", "rb"), delimiter=",", skiprows=0)
sys.path.append('../Helper/DataShow')
from  DataShow import DataShow as DS
show = DS()
test_matrix = np.loadtxt(open(r"E:\OneDrive\Python\BHand\Data\SF\Tilt\0D\MW\Failed\TMW75.csv","rb"),delimiter=",",skiprows=0)
test_matrix1 = np.loadtxt(open(r"E:\OneDrive\Python\BHand\Data\SF\Tilt\0D\MW\Success\TMW73.csv","rb"),delimiter=",",skiprows=0)
test_matrix2 = np.loadtxt(open(r"E:\OneDrive\Python\BHand\Data\SF\Tilt\0D\MW\Success\TMW2S.csv","rb"),delimiter=",",skiprows=0)
test_matrix3 = np.loadtxt(open(r"E:\OneDrive\Python\BHand\Data\SF\Tilt\0D\MW\Success\TMW2S.csv","rb"),delimiter=",",skiprows=0)
none = np.loadtxt(open(r"E:\OneDrive\Python\BHand\Data\SF\Tilt\0D\MW\Success\TMW2S.csv","rb"),delimiter=",",skiprows=0)
show.PlotShow(test_matrix,test_matrix1,test_matrix2,test_matrix3)