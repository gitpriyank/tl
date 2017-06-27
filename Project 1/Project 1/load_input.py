import numpy as np
from sklearn import tree
import csv
import sys

filepath = "/home/vppriyank/pycharm/pycharm-edu-3.5/bin/SkLearnDecisionTree/resources/2EXAMPLE_DATASET_HACKATHON2017.csv"
#filepath= sys.argv[1]
total_rows_count = 0


clf = tree.DecisionTreeClassifier()

with open(filepath, 'r') as file:
    total_rows_count = len(list(csv.reader(file, delimiter=',')))

training_rows_count  = int(total_rows_count*0.8)
test_rows_count = total_rows_count - training_rows_count

training_rows= np.genfromtxt(filepath
                         ,delimiter=',', usecols=(0,1,2,3,4,5,6,7,8), max_rows=training_rows_count, skip_header=1)

test_rows =  np.genfromtxt(filepath
                         ,delimiter=',', usecols=(0,1,2,3,4,5,6,7,8), max_rows=test_rows_count, skip_header=training_rows_count)

# print(training_rows)
# print(test_rows.ndim)
# print(training_rows.size)
