from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
import pandas as pd

data_set = pd.read_csv('2EXAMPLE_DATASET_HACKATHON2017.csv', header = 1, sep=',')

X = data_set.values[1:,:9]
Y = data_set.values[1:,11]

x_train, x_test, y_train, y_test = train_test_split (X, Y, test_size = 0.2, random_state = 100)

clf = GradientBoostingClassifier(n_estimators = 100, learning_rate = 1.0, max_depth = 2, random_state = 0).fit(x_train, y_train)

output = clf.predict(x_test)
print(output)
accuracy = clf.score(x_train, y_train)
print(accuracy)
