import numpy as np
#import sys
from sklearn import tree
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score

from sklearn.preprocessing import Imputer



input_filepath = "/home/vppriyank/Desktop/Team 22/CART/time series/std_dataset.csv"
output_filepath ="/home/vppriyank/Desktop/Team 22/CART/time series/output.csv"

training_rows = []
test_rows = []

for i in range(0,6):
    training_rows.append(np.genfromtxt(input_filepath
                         ,delimiter=',', usecols=[x for x in range(0,60)],
                         skip_header= i*100,
                         max_rows= 80))

for i in range(0,6):
    test_rows.append(np.genfromtxt(input_filepath
                         ,delimiter=',', usecols=[x for x in range(0,60)],
                         skip_header= i*100 + 80,
                         max_rows= 20))


output_rows = np.genfromtxt(output_filepath
                         ,delimiter=',', usecols=(0),
                         dtype=str,
                         max_rows=480)

training_rows =  np.concatenate(tuple(training_rows), axis =0)
test_rows = np.concatenate(tuple(test_rows), axis =0)


imp = Imputer(missing_values='NaN', strategy='mean', axis=0)


#Training
clf = tree.DecisionTreeClassifier()
clf.fit(imp.fit_transform(training_rows), output_rows)

print("Some random prediction")
print(clf.predict([[24.7991,32.178,31.9929,26.146,34.9435,28.3831,25.8137,30.6544,35.0456,24.4443,33.0376,33.1228,32.4207,27.0248,26.0678,24.8578,32.8041,25.8104,33.2183,31.0734,33.1783,34.5822,29.0408,26.287,24.4025,30.6871,33.1798,30.3276,29.5847,27.9318,25.5614,33.3619,29.6724,30.578,25.7439,30.0951,30.8266,31.2658,45.6125,45.2926,45.943,46.323,52.0274,51.0844,45.7017,43.8002,45.1986,42.7735,48.093,45.9889,52.9664,41.7357,41.3109,45.6565,50.4987,51.4704,41.3267,41.8286,50.3147,47.7541]]))

predicted_outputs = []

#Testing all 120 values
for test_instance in range(0, 120):
    predicted_output = clf.predict(imp.fit_transform(test_rows)[test_instance: test_instance + 1])[0]
    print("predicted output {0} is {1}".format(test_instance+1,predicted_output))

    predicted_outputs.append([[predicted_output]])


predicted_outputs = np.concatenate(tuple(predicted_outputs), axis = 0)

expected_outputs =[]

for i in range(0,120):
    if(i<20) and (i>=0):
        expected_outputs.append([['normal']])
    elif(i<40) and (i>=20):
        expected_outputs.append([['cyclic']])
    elif(i<60) and (i>=40):
        expected_outputs.append([['increase']])
    elif(i<80) and (i>=60):
        expected_outputs.append([['decrease']])
    elif(i<100) and (i>=80):
        expected_outputs.append([['upward']])
    elif(i<120) and (i>=100):
        expected_outputs.append([['downward']])


expected_outputs = np.concatenate(tuple(expected_outputs), axis =0)


cnf_matrix = confusion_matrix(expected_outputs, predicted_outputs, labels=np.array(['normal', 'cyclic', 'increase', 'decrease', 'upward', 'downward']))

score = accuracy_score(expected_outputs, predicted_outputs)

p_score = precision_score(expected_outputs, predicted_outputs, average='weighted')


print("confusion matrix =")
print(cnf_matrix)

print("accuracy score = {}".format(score))

print("precision score = {}".format(p_score))
