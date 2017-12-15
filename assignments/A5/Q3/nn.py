import sys
import io
from numpy import *
from sklearn.linear_model import *
from sklearn.metrics import *
from sklearn.neighbors import *

if len(sys.argv) != 2:
    print "Usage: python nn.py <ratings_csv_file>"
    print "Example: python nn.py ratings.csv "
    exit()
    
ratings = genfromtxt(sys.argv[1], delimiter=',', skip_header=1, usecols=range(3))
random.shuffle(ratings)
train, test = ratings[len(ratings)/10:, :], ratings[:len(ratings)/10, :]
neighbors = KNeighborsClassifier(n_neighbors=1)
neighbors.fit(train, train[:, 0])
distances, neighbors_indices = neighbors.kneighbors(test)
euclidean_neighbors = array([train[ns[0]] for ns in neighbors_indices])
linear_reg = LinearRegression()
linear_reg.fit(train, train[:, 0])
neighbors_idx = linear_reg.predict(test)
pearson_neighbors = array([train[int(idx)] for idx in neighbors_idx])
y_true = []
for user, movie, rating in test:
        y_true.append(rating)
y_pred_euc = []
for user, movie, rating in euclidean_neighbors:
        y_pred_euc.append(rating)
y_pred_pear = []
for user, movie, rating in pearson_neighbors:
        y_pred_pear.append(rating)

print 'Euclidean MSE:'
print mean_squared_error(y_true, y_pred_euc)
print '-----------------'
print 'Pearson MSE:'
print mean_squared_error(y_true, y_pred_pear)

