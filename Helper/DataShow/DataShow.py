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
    def ImgineShow(self,Matrix_data):
        plt.imshow(Matrix_data)
        plt.show()
