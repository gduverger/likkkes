# Code source: Jaques Grobler
# License: BSD 3 clause

import sys
import json
import numpy

from csv import reader
from sklearn import datasets
from sklearn import linear_model
from sklearn.preprocessing import normalize, scale

TEST_SIZE = 10 # in percent
FILE_NAME = 'csv/shots.date_20150214-timeframe_week-sort_None-shots_len_5600.20150319-184254.no_location.csv'

# Load the dataset
data = numpy.loadtxt(open(FILE_NAME, 'r'), delimiter=',', skiprows=1, usecols=(1, 3, 4, 5, 6, 9, 10, 11))
target = numpy.loadtxt(open(FILE_NAME, 'r'), delimiter=',', skiprows=1, usecols=(2,))

# Scale
data = scale(data, axis=0)
target = scale(target, axis=0)

# Normalize
data = normalize(data, axis=0)
target = numpy.array([float(i)/sum(target) for i in target])

test_size = len(data)*TEST_SIZE/100

# Split the data into training/testing sets
data_train = data[:-test_size]
data_test = data[-test_size:]

# Split the targets into training/testing sets
target_train = target[:-test_size]
target_test = target[-test_size:]

# Create linear regression object
regression = linear_model.LinearRegression()

# Train the model using the training sets
regression.fit(data_train, target_train)

# The coefficients
print('Coefficients: \n', [_ for _ in regression.coef_])

# The mean square error
# print('Residual sum of squares: %.2f' % numpy.mean((regression.predict(data_test) - target_test) ** 2))

# Explained variance score: 1 is perfect prediction
print('Score: %.2f' % regression.score(data_test, target_test))
