import numpy as np
import csv
from sklearn import tree
import load_input as lp
from sklearn.metrics import confusion_matrix

#filepath = "/home/vppriyank/pycharm/pycharm-edu-3.5/bin/SkLearnDecisionTree/resources/2EXAMPLE_DATASET_HACKATHON2017_CSV.csv"
total_rows_count = 0

for output in range(9, 12):
    success = 0
    print("calculating accuracy for %d column" % output)
    output1 = np.genfromtxt(lp.filepath
                            , delimiter=',', usecols=(output), max_rows=lp.training_rows_count, skip_header=1, dtype=str)

    expected_outputs = np.genfromtxt(lp.filepath
                                    , delimiter=',', usecols=(output), max_rows=lp.test_rows_count,
                                     skip_header=lp.training_rows_count, dtype=str)

    lp.clf.fit(lp.training_rows, output1)
    predicted_outputs=[]
    for i in range(0, lp.test_rows_count):
            test_row = lp.test_rows[i : i + 1 ]
            predicted_output = lp.clf.predict(test_row)
            predicted_outputs.append(predicted_output)
            if(predicted_output[0] == expected_outputs[i]):
                success += 1
    #predicted_outputs = np.concatenate(tuple(predicted_outputs), axis=0)
    #expected_outputs = np.concatenate(tuple(expected_outputs), axis=0)
    #cnf_matrix = confusion_matrix(expected_outputs, predicted_outputs)
    #print ("Confusion Matrix for row", cnf_matrix)
            #feedback is reducing accuracy
    #lp.clf.fit(np.concatenate((lp.training_rows, test_row), axis=0), np.concatenate((output1, predicted_output), axis=0))

    print("total = %d" % (lp.test_rows_count))
    print("success = %d" % (success))
    print("accuracy = %d percentage" % (success/lp.test_rows_count * 100) )
#predicted_outputs = np.concatenate(tuple(predicted_outputs), axis=0)
#expected=expected_outputs.T
#expected_outputs = np.concatenate(tuple(expected_outputs), axis=0)
#cnf_matrix = confusion_matrix(expected, predicted_outputs)
#print ("Confusion Matrix for row", i, cnf_matrix)




#visualize_tree(clf, ['N1',' N2', 'N3', 'N4', 'N5','N6', 'N7', 'N8','N9'])
