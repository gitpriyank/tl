import sys
#sys.path.append("/home/vppriyank/hackathon/dev_env/lib/python3.5/site-packages/")
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import csv
#from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
#import 02m

try:
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    server = modbus_tcp.TcpServer()
    logger.info("running...")
    logger.info("enter 'quit' for closing the server")

    server.start()

    slave_1 = server.add_slave(1)
    slave_1.add_block('TL', cst.READ_HOLDING_REGISTERS, 0, 1000)

    #slave_2 = server.add_slave(2)
    #slave_2.add_block(2, cst.READ_HOLDING_REGISTERS, 0, 200)

    #slave_3 = server.add_slave(3)
    #slave_3.add_block(3, cst.READ_HOLDING_REGISTERS, 0, 200)

    def set_value(value, address):
        slave = server.get_slave(1)
        slave.set_values('TL', address, value)

    filepath = '/home/vppriyank/Desktop/Project 1/2EXAMPLE_DATASET_HACKATHON2017.csv'

    clf = GradientBoostingClassifier(n_estimators = 100, learning_rate = 1.0, max_depth = 2, random_state = 0)

    with open(filepath, 'r') as file:
        total_rows_count = len(list(csv.reader(file, delimiter=',')))
        training_rows_count = int(0.8 * total_rows_count)
        test_rows_count = int(total_rows_count - training_rows_count)

    training_rows = np.genfromtxt(filepath, delimiter=',', usecols=(0,1,2,3,4,5,6,7,8), skip_header=1, max_rows=training_rows_count)
    test_rows = np.genfromtxt(filepath, delimiter=',', usecols=(0,1,2,3,4,5,6,7,8), skip_header=training_rows_count, max_rows=test_rows_count)

    for output in range(9, 12):
        success = 0
        if output == 9:
           addrs = 0
        elif output == 10:
           addrs = 201
        elif output == 11:
           addrs = 401
        #slave_id = output - 8
        #name = output - 8
        output1 = np.genfromtxt(filepath, delimiter=',', usecols=(output), skip_header=1, max_rows = training_rows_count, dtype=str)
        expected_outputs = np.genfromtxt(filepath, delimiter=',', usecols=(output), skip_header=training_rows_count, max_rows=test_rows_count, dtype=str)

        predicted_outputs = []

        clf.fit(training_rows, output1)
        for i in range(0, test_rows_count - 1):
            test_row = test_rows[i : i + 1]
            predicted_output = clf.predict(test_row)
            predicted_outputs.append(predicted_output)
            #set_value(predicted_output, i, slave_id, name)
            if(predicted_output[0] == expected_outputs[i]):
                success += 1
        predicted_outputs = np.concatenate(tuple(predicted_outputs), axis = 0)
        for i in range (0, test_rows_count -1):
            set_value(int(predicted_outputs[i]), addrs)
            addrs += 1
        #print(predicted_outputs)
        print("total = %d" % (test_rows_count))
        print("success = %d" % (success))
        print("accuracy = %d percentage" % (success/test_rows_count * 100) )

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
             sys.stdout.write("unknown command %s\r\n" % args[0])

finally:
    server.stop()

