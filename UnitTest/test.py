import sys
sys.path.append('../HandAssembly')
sys.path.append('../Helper/DataToCSV')
import time
import os
import matplotlib.pyplot as plt
import matplotlib as cm
from HandFunc import Hand,HandSensor,SensorShow
from DataToCSV import CSVRecord
from mpl_toolkits.mplot3d  import Axes3D
import numpy as np


hand = Hand()
sensor=SensorShow()
hand.CloseSpeedControl()