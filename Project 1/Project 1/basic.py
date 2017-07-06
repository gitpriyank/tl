import socket
import struct
import time
import subprocess, os

#os.system('sudo ./diagslave -m tcp')
subprocess.call(['sudo', './diagslave', '-m', 'tcp'], shell=False)
# Create a TCP/IP socket
TCP_IP = '127.0.0.1'
TCP_PORT = 502
BUFFER_SIZE = 39
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

try:
    # Switch Plug On then Off
    unitId = 1 # Plug Socket, slaveID
    functionCode = 5 # Write coil
    print("\nSwitching Plug ON...")
    coilId = 0
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
    sock.send(req)
    print("TX: (%s)" %req)
    #rec = sock.recv(BUFFER_SIZE)
    #print("RX: (%s)" %rec)
    time.sleep(2)

    """print("\nSwitching Plug OFF...")
    coilId = 2
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
    sock.send(req)
    print("TX: (%s)" %req)
    rec = sock.recv(BUFFER_SIZE)
    print("RX: (%s)" %rec)
    time.sleep(2)"""

finally:
    print('\nCLOSING SOCKET')
    sock.close()
