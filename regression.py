# Code source: Jaques Grobler
# License: BSD 3 clause

"""
							Coefficients				Scaled					Normalized				Scaled & Normalized
0. shot_id					
1. views_count				0.038799469117713536		0.437757106251219		0.012098724771760924	-32215800673578.172		#1
2. likes_count
3. comments_count			2.6295230337200826			0.21547098766519121		0.0060969455532719945	-15857127823705.281		#3
4. attachments_count		-2.9295888525769791			-0.032675927993685905	-0.00088190105952418401	2404715235998.0898 		#8
5. rebounds_count			1.0810508912912913			0.0047219639505726579	0.0001223461585673363	-347502866880.20605		#7
6. buckets_count			2.0683099655388761			0.27873912497288866		0.0072973086985065458	-20513211463209.656		#2
7. created_at
8. user_id
9. user_followers_count		0.0027358793437922534		0.11946709786308196		0.0031572606636933427	-8791926291652.709		#4
10. user_followings_count	0.0012460953875700772		0.0066838191194368152	0.00021576205757785002	-491881414179.625		#6
11. user_shots_count		0.034741807707363175		0.052996412852846522	0.0016542944231239427	-3900157983733.9443		#5

Score: 0.90

"""

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
