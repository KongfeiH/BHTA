import numpy as np



class CSVRecord():
    def __init__(self):
        pass
    def Record(self,fileSite,np_Matrix):
       # filename = fileSite+".csv"
       # with open(filename,"w") as file_object:
       #     file_object.write()

       np.savetxt(fileSite+".csv", np_Matrix, delimiter=',')
