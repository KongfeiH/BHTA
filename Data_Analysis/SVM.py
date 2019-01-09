import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets


iris =datasets.load_iris()

x=iris.data
y=iris.target
x=x[y<2,:2]
y=y[y<2]

print(x,y)
plt.scatter(x[y==0,0],x[y==0,1],color='red')
plt.scatter(x[y==1,0],x[y==1,1],color='blue')
plt.show()


from sklearn.preprocessing import StandardScaler
standscaler=StandardScaler()
standscaler.fit(x)
x_standard=standscaler.transform(x)

from sklearn.svm import  LinearSVC

svc =LinearSVC(C=1e9)
svc.fit(x_standard,y)
print(svc.coef_)
