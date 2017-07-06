import sys
#sys.path.append("/home/vppriyank/hackathon/dev_env/lib/python3.5/site-packages/")
import numpy as np
from sklearn import tree
import csv
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

try:
    print ('Training column Number: ')
    cmd = sys.stdin.readline()
    args = cmd.split(' ')
    training_columns = []
    for val in args[0:]:
        training_columns.append(int(val.rstrip('\n')))
    print('Output column Number: ')
    cmd = sys.stdin.readline()
    args = cmd.split(' ')
    output_columns = []
    for val in args[0:]:
        output_columns.append(int(val.rstrip('\n')))

    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    server = modbus_tcp.TcpServer(address='127.0.0.1')
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

    clf = tree.DecisionTreeClassifier()

    with open(filepath, 'r') as file:
        total_rows_count = len(list(csv.reader(file, delimiter=',')))
        training_rows_count = int(input('No. of Training rows= '))
        test_rows_count = int(total_rows_count - training_rows_count)

    training_rows = np.genfromtxt(filepath, delimiter=',', usecols=(training_columns), skip_header=1, max_rows=training_rows_count)
    test_rows = np.genfromtxt(filepath, delimiter=',', usecols=(training_columns), skip_header=training_rows_count, max_rows=test_rows_count)

    predicted_outputsM1 = []
    predicted_outputsM2 = []
    predicted_outputsM3 = []

    print('Training...')

    for output in output_columns:
        print('Testing...')
        success = 0
        #slave_id = output - 8
        #name = output - 8
        output1 = np.genfromtxt(filepath, delimiter=',', usecols=(output), skip_header=1, max_rows = training_rows_count, dtype=str)
        expected_outputs = np.genfromtxt(filepath, delimiter=',', usecols=(output), skip_header=training_rows_count, max_rows=test_rows_count, dtype=str)

        clf.fit(training_rows, output1)
        for i in range(0, test_rows_count - 1):
            test_row = test_rows[i : i + 1]
            predicted_output = clf.predict(test_row)
            if output == 9:
                predicted_outputsM1.append(predicted_output)
            elif output == 10:
                predicted_outputsM2.append(predicted_output)
            elif output == 11:
                predicted_outputsM3.append(predicted_output)
            #set_value(predicted_output, i, slave_id, name)
            if(predicted_output[0] == expected_outputs[i]):
                success += 1

    print('Done. Sending data...')

    predicted_outputsM1 = np.concatenate(tuple(predicted_outputsM1), axis = 0)
    predicted_outputsM2 = np.concatenate(tuple(predicted_outputsM2), axis = 0)
    predicted_outputsM3 = np.concatenate(tuple(predicted_outputsM3), axis = 0)

    addrs = 0

    for i in range (0, test_rows_count -1):
        set_value(int(predicted_outputsM1[i]), addrs)
        set_value(int(predicted_outputsM2[i]), addrs+1)
        set_value(int(predicted_outputsM3[i]), addrs+2)
        addrs += 3
    print('Data Sent')
    '''print([predicted_outputsM1, predicted_outputsM2, predicted_outputsM3])
        print("total = %d" % (test_rows_count))
        print("success = %d" % (success))
        print("accuracy = %d percentage" % (success/test_rows_count * 100) )
    print(predicted_outputsM1)
    print(predicted_outputsM2)
    print(predicted_outputsM3)'''
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

