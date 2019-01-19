import matplotlib.pyplot as plt
import matplotlib as cm
import numpy as np


class DataShow():
    def __init__(self):
        pass
    def ImgineShow_Dynamic(self,Matrix_data):#This function has a bug now
        fig = plt.figure()
        plt.ion()
        while True:
            plt.clf()
            ax = fig.add_subplot(111)
            ax.imshow(Matrix_data)
            plt.pause(0.33)
            plt.ioff()
    def ImgineShow(self,Matrix_data,Matrix_data1=0,Matrix_data2=0,Matrix_data3=0,Matrix_data4=0,Matrix_data5=0,n=1):
        if   n==1:
             plt.imshow(Matrix_data)
             plt.show()
        elif n==2:
            fig = plt.figure()
            ax = fig.add_subplot(121)
            ax.imshow(Matrix_data)
            ax1 = fig.add_subplot(122)
            ax1.imshow(Matrix_data1)
            plt.show()
        elif n==3:
            fig = plt.figure()
            ax = fig.add_subplot(221)
            ax.imshow(Matrix_data)
            ax1 = fig.add_subplot(222)
            ax1.imshow(Matrix_data1)
            ax2 = fig.add_subplot(223)
            ax2.imshow(Matrix_data2)
            plt.show()
        elif n==4:
            fig = plt.figure()
            ax = fig.add_subplot(221)
            ax.imshow(Matrix_data)
            ax1 = fig.add_subplot(222)
            ax1.imshow(Matrix_data1)
            ax2 = fig.add_subplot(223)
            ax2.imshow(Matrix_data2)
            ax3 = fig.add_subplot(224)
            ax3.imshow(Matrix_data3)
            plt.show()
        elif n==6:
            fig = plt.figure()
            ax = fig.add_subplot(321)
            ax.imshow(Matrix_data)
            ax1 = fig.add_subplot(322)
            ax1.imshow(Matrix_data1)
            ax2 = fig.add_subplot(323)
            ax2.imshow(Matrix_data2)
            ax3 = fig.add_subplot(324)
            ax3.imshow(Matrix_data3)
            ax4 = fig.add_subplot(325)
            ax4.imshow(Matrix_data4)
            ax4 = fig.add_subplot(326)
            ax4.imshow(Matrix_data5)
            plt.show()
    def PlotShow(self,Matrix_data,Matrix_data1,Matrix_data2,Matrix_data3):
        fig = plt.figure()
        ax = fig.add_subplot(211)
        ax.plot(Matrix_data)
        ax1 = fig.add_subplot(212)
        ax1.plot(Matrix_data1)
       # ax2 = fig.add_subplot(223)
       # ax2.plot(Matrix_data2)
       # ax2 = fig.add_subplot(224)
       # ax2.plot(Matrix_data3)
        plt.xlabel("Time 0.1/s")
        plt.ylabel("N")
        plt.show()

