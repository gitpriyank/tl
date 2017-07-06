import multiprocessing
# import time
# import sys
# sys.path.append("/home/vppriyank/hackathon/dev_env/lib/python3.5/site-packages/")
import numpy as np
from sklearn import tree
import csv
# from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

try:
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    server = modbus_tcp.TcpServer()
    logger.info("running...")
    logger.info("enter 'quit' for closing the server")

    server.start()

    slave_1 = server.add_slave(1)
    slave_1.add_block('TL', cst.READ_HOLDING_REGISTERS, 0, 1000)

    # slave_2 = server.add_slave(2)
    # slave_2.add_block(2, cst.READ_HOLDING_REGISTERS, 0, 200)

    # slave_3 = server.add_slave(3)
    # slave_3.add_block(3, cst.READ_HOLDING_REGISTERS, 0, 200)

    def set_value(value, address):
        slave = server.get_slave(1)
        slave.set_values('TL', address, value)

    filepath = '/home/vppriyank/Desktop/Project 1/2EXAMPLE_DATASET_HACKATHON2017.csv'

    clf = tree.DecisionTreeClassifier()

    with open(filepath, 'r') as file:
        total_rows_count = len(list(csv.reader(file, delimiter=',')))
        training_rows_count = int(0.8 * total_rows_count)
        test_rows_count = int(total_rows_count - training_rows_count)

    training_rows = np.genfromtxt(filepath, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8), skip_header=1, max_rows=training_rows_count)
    test_rows = np.genfromtxt(filepath, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8), skip_header=training_rows_count, max_rows=test_rows_count)


    def m1():
        predicted_outputs_m1 = []
        success = 0
        output1 = np.genfromtxt(filepath, delimiter=',', usecols=9, skip_header=1, max_rows=training_rows_count, dtype=str)
        expected_outputs = np.genfromtxt(filepath, delimiter=',', usecols=9, skip_header=training_rows_count, max_rows=test_rows_count, dtype=str)
        clf.fit(training_rows, output1)
        for i in range(0, test_rows_count - 1):
            test_row = test_rows[i: i + 1]
            predicted_output = clf.predict(test_row)
            # predicted_outputs_m1.append(predicted_output)
            # predicted_outputs_m1 = np.concatenate(tuple(predicted_outputs_m1), axis=0)
            addrs = 0
            set_value(predicted_output, addrs)
            addrs += 1
            if predicted_output[0] == expected_outputs[i]:
                    success += 1
        print("Total = %d" % test_rows_count)
        print("success = %d" % success)
        print("accuracy for M1 = %d percentage" % (success/test_rows_count * 100))

    def m2():
        predicted_outputs_m2 = []
        success = 0
        output1 = np.genfromtxt(filepath, delimiter=',', usecols=10, skip_header=1, max_rows=training_rows_count, dtype=str)
        expected_outputs = np.genfromtxt(filepath, delimiter=',', usecols=10, skip_header=training_rows_count, max_rows=test_rows_count, dtype=str)
        clf.fit(training_rows, output1)
        for i in range(0, test_rows_count - 1):
            test_row = test_rows[i: i + 1]
            predicted_output = clf.predict(test_row)
            # predicted_outputs_m2.append(predicted_output)
            # predicted_outputs_m2 = np.concatenate(tuple(predicted_outputs_m2), axis = 0)
            addrs = 201
            set_value(predicted_output, addrs)
            addrs += 1
            if predicted_output[0] == expected_outputs[i]:
                    success += 1
        print("Total = %d" % test_rows_count)
        print("success = %d" % success)
        print("accuracy for M2 = %d percentage" % (success/test_rows_count * 100))

    def m3():
        predicted_outputs_m3 = []
        success = 0
        output1 = np.genfromtxt(filepath, delimiter=',', usecols=11, skip_header=1, max_rows = training_rows_count, dtype=str)
        expected_outputs = np.genfromtxt(filepath, delimiter=',', usecols=11, skip_header=training_rows_count, max_rows=test_rows_count, dtype=str)
        clf.fit(training_rows, output1)
        for i in range(0, test_rows_count - 1):
            test_row = test_rows[i: i + 1]
            predicted_output = clf.predict(test_row)
            # predicted_outputs_m3.append(predicted_output)
            # predicted_outputs_m3 = np.concatenate(tuple(predicted_outputs_m3), axis = 0)
            addrs = 401
            set_value(predicted_output, addrs)
            addrs += 1
            if predicted_output[0] == expected_outputs[i]:
                    success += 1
        print("Total = %d" % test_rows_count)
        print("success = %d" % success)
        print("accuracy for M3 = %d percentage" % (success/test_rows_count * 100))

    '''def cmd():
        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if args[0] == 'get_values':
                            slave_id = int(args[1])
                            name = args[2]
                            address = int(args[3])
                            length = int(args[4])
                            slave = server.get_slave(slave_id)
                            values = slave.get_values(name, address, length)
                            sys.stdout.write('done: values read: %s\r\n' % str(values))

            elif cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break

            else:
                 sys.stdout.write("unknown command %s\r\n" % args[0])'''

finally:
    server.stop()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=m1)
    p2 = multiprocessing.Process(target=m2)
    p3 = multiprocessing.Process(target=m3)
    # p4 = multiprocessing.Process(target=cmd)
    p1.start()
    p2.start()
    p3.start()
    # p4.start()
    p1.join()
    p2.join()
    p3.join()
    # p4.join()
    print('Done')
