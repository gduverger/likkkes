import sys
import json
import numpy

from sklearn.cluster import KMeans
# from sklearn.preprocessing import scale

NUMBER_OF_CLUSTERS = 8
FILE_NAME = 'date_20150214-timeframe_week-sort_None-shots_len_5600.20150319-184254'

data = numpy.loadtxt(open('csv/likes.%s.csv' % FILE_NAME.lower(), 'rb'), delimiter=',')
# 			| user_1	| user_2	| ... (3715)
# ---------------------------------------
# shot_1	| 1			| 0			| ...
# shot_2	| 1			| 0			| ...
# ...
# (3715)

data = [list(i) for i in zip(*data)]
# 			| shot_1	| shot_2	| ... (623)
# ---------------------------------------
# user_1	| 1			| 1			| ...
# user_2	| 0			| 0			| ...
# ...
# (3715)

#data = scale(data)

n_samples, n_features = numpy.array(data).shape
# n_samples: 3715 (users)
# n_features: 623 (shots)

kmeans = KMeans(init='k-means++', n_clusters=NUMBER_OF_CLUSTERS)

clusters_file = open('csv/clusters.%s.number_clusters_%s.csv' % (FILE_NAME.lower(), NUMBER_OF_CLUSTERS), 'w')
clusters_file.write(','.join([str(_) for _ in kmeans.fit_predict(data)]))
# [cluster_1, cluster_2, cluster_1...] (3715)
