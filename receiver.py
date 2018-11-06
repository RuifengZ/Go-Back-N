import socket
import sys
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
    print('expecting: ' + str(expect_seq))
    print('got pkt: ' + str(seq))

    if ip_checksum(pkt) == checksum and seq == str(expect_seq):
        print('recv: Good Data Sending ACK' + str(seq))
        # print('recv pkt: ' + str(pkt))
        s.sendto(str(expect_seq).encode(), addr)
        expect_seq += 1
    else:
        # Check seq and send according ACK
        print('recv: Sending ACK' + str(expect_seq))
        s.sendto(str(expect_seq).encode(), addr)
s.close()
