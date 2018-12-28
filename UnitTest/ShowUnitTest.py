import sys
import numpy as np
sys.path.append('../Helper/DataShow')
from  DataShow import DataShow as DS

show = DS()
show.ImgineShow_Dynamic(np.arange(600).reshape(20,30))