import numpy as np
import scipy.cluster.hierarchy as hac

a = np.array([[-4, -2],
              [-3, -2],
              [-2, -2],
              [-1, -2],
              [1, -1],
              [1, 1],
              [2, 3],
              [3, 2],
              [3, 4],
              [4, 3]])

for method in ['single', 'complete', 'average', 'centroid', 'ward']:
	z = hac.linkage(a, method=method)
	z1 = hac.fcluster(z, 3, criterion='maxclust')
	print 'Clustering Method: ', method
	for i in range(0, len(z1)):
		print 'Cluster: ', z1[i], a[i]
