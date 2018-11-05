import socket
import sys
import time
from check import ip_checksum

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 2163  # Arbitrary non-privileged port

# Datagram (udp) socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

expect_seq = 0
N = input('Enter Window Size: ')

# now keep talking with the client
while 1:
    # receive data from client (data, addr)
    data, addr = s.recvfrom(1024)

    checksum = data[:2]
    seq = data[2]
    pkt = data[3:]

    if not data:
        break
    # print(str(ip_checksum(pkt) == checksum))

    if ip_checksum(pkt) == checksum and seq == str(expect_seq):
        print('recv: Good Data Sending ACK' + str(seq))
        print('recv pkt: ' + str(pkt))
        s.sendto(str(seq), addr)
        expect_seq = 1 - expect_seq
    else:
        # Check seq and send according ACK
        if seq == str(expect_seq):
            print('recv: Bad Checksum Not Sending')
        else:
            print('recv: Bad Seq Sending ACK' + str(1 - expect_seq))
            s.sendto(str(1 - expect_seq), addr)
s.close()
