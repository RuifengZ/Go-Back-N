import socket  # for sockets
import sys  # for exit
from socket import timeout
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 2163

s.settimeout(3)
seq = 0

checksum_test = True

# Send 7 test messages
for i in range(7):
    msg = 'Message ' + str(i)
    ack_received = False
    while not ack_received:
        try:
            # Test bad checksum on message 3
            if i == 3 and checksum_test:
                print('send: TESTING BAD CHECKSUM')
                s.sendto(ip_checksum("wrong") + str(seq) + msg, (host, port))
                checksum_test = False
            # Send good package
            else:
                print('send: SENDING PKT')
                s.sendto(ip_checksum(msg) + str(seq) + msg, (host, port))
        except socket.error as msg:
            print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        try:
            # receive data from client (data, addr)
            print('send: GETTING ACK')
            reply, addr = s.recvfrom(1024)
            ack = reply[0]
        except timeout:
            print('send: TIMEOUT')
        else:
            print('Checking for ACK ' + str(seq))
            if ack == str(seq):
                ack_received = True
    print('ACK FOUND, CHANGING SEQ')
    seq = 1 - seq
