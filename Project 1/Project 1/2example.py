import numpy as np
from sklearn import tree
import csv
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
import sys
from mlxtend.plotting import plot_confusion_matrix
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt
train_filepath = sys.argv[1]
test_filepath = sys.argv[2]

# train_filepath = "/home/deepa_panicker/smart_india_hackathon/SkLearnDecisionTree/dataset/dscdsc.csv"
# test_filepath="/home/deepa_panicker/smart_india_hackathon/SkLearnDecisionTree/dataset/2EXAMPLE_DATASET_HACKATHON2017.csv"
total_rows_count = 0


clf = tree.DecisionTreeClassifier()
with open(train_filepath, 'r') as file:
    training_rows_count = len(list(csv.reader(file, delimiter=',')))

with open(test_filepath, 'r') as file:
    test_rows_count = len(list(csv.reader(file, delimiter=',')))


training_rows= np.genfromtxt(train_filepath
                         ,delimiter=',', usecols=(0,1,2,3,5,7), skip_header=1)

test_rows =  np.genfromtxt(test_filepath
                         ,delimiter=',', usecols=(0,1,2,3,5,7), skip_header=1)


for output in range(9, 12):
    success = 0
    print("calculating accuracy for %d row" % output)
    output1 = np.genfromtxt(train_filepath
                            , delimiter=',', usecols=(output), skip_header=1, dtype=str)

    expected_outputs = np.genfromtxt(test_filepath
                                     , delimiter=',', usecols=(output),
                                     skip_header=1, dtype=str)
    predicted_outputs = []

    # print(test_rows_count)
    # print(training_rows_count)
    clf.fit(training_rows, output1)
    for i in range(0, test_rows_count -1):
        test_row = test_rows[i : i + 1 ]
        # print(test_row)
        predicted_output = clf.predict(test_row)
        predicted_outputs.append(predicted_output)
        if(predicted_output[0] == expected_outputs[i]):
            success += 1
        #feedback is reducing accuracy
        #clf.fit(np.concatenate((training_rows, test_row), axis=0), np.concatenate((output1, predicted_output), axis=0))
    predicted_outputs = np.concatenate(tuple(predicted_outputs),axis=0)

    print("total = %d" % (test_rows_count))
    print("success = %d" % (success))
    print("accuracy = %d percentage" % (success/test_rows_count * 100) )

    print("Confusion matrix for output {}".format(output))
    cnf_matrix = confusion_matrix(expected_outputs, predicted_outputs, labels=np.array(['RAISE', 'LOWER', 'HOLD', 'STOP']))
    print(cnf_matrix)

    score = accuracy_score(expected_outputs, predicted_outputs)
    print("Accuracy score = {}".format(score))

    fig, ax = plot_confusion_matrix(conf_mat = cnf_matrix)
    plt.show()
