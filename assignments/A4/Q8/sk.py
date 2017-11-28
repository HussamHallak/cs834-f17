import sys
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print "Usage: python k.py <K value>"
    print "Example: python k.py 3"
    exit()

 
x = np.array([-4, -3, -2, -1, 1, 1, 2, 3, 3, 4])
y = np.array([-2, -2, -2, -2, -1, 1, 3, 2, 4, 3])
 
plt.plot()
plt.xlim([-5, 5])
plt.ylim([-5, 5])
plt.title('Scatter Plot', fontsize=20)
plt.xlabel('X', fontsize=20)
plt.ylabel('Y', rotation=0, fontsize=20)
plt.scatter(x, y)
plt.show()
 
# create new plot and data
plt.plot()
X = np.array(list(zip(x, y))).reshape(len(x), 2)
colors = ['b', 'g', 'r', 'c']
markers = ['o', 'v', 's', 'h']
 
# KMeans algorithm 
K = int(sys.argv[1])
from spherecluster import SphericalKMeans
kmeans_model = SphericalKMeans(n_clusters=K).fit(X)
 
plt.plot()
for i, l in enumerate(kmeans_model.labels_):
    plt.plot(x[i], y[i], color=colors[l], marker=markers[l],ls='None')
    plt.xlim([-5, 5])
    plt.ylim([-5, 5])
 
plt.title('Scatter Plot', fontsize=20)
plt.xlabel('X', fontsize=20)
plt.ylabel('Y', rotation=0, fontsize=20)
plt.scatter(x, y)
plt.show()
