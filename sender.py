import socket  # for sockets
import sys  # for exit
import time
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

N = input('Enter Window Size: ')
base = 0
nextSeq = 0
startTime = time.time()

testLoss = True

# Continuously send packets
while 1:
    print('base: ' + str(base) + ' nextSeq: ' + str(nextSeq))
    if nextSeq < base + N:
        try:
            # Send good package
            msg = 'Message ' + str(nextSeq)
            if nextSeq == 2 and testLoss:
                print('TESTING PACKET LOSS')
                testLoss = False
            else:
                print('send: SENDING PKT: ' + str(nextSeq))
                s.sendto(ip_checksum(msg) + str(nextSeq) + msg, (host, port))
            if base == nextSeq:
                startTime = time.time()
            nextSeq += 1
        except socket.error as msg:
            print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

    if time.time() - startTime > 3:
        print('----TIMEOUT----')
        startTime = time.time()
        for j in range(base, nextSeq):
            prevMsg = 'Message ' + str(j)
            s.sendto(ip_checksum(prevMsg) + str(j) + prevMsg, (host, port))

    try:
        # receive data from client (data, addr)
        reply, addr = s.recvfrom(1024)
        ack = reply[0]
        print('Got ACK: ' + ack)
        base = int(ack) + 1
        # if base == nextSeq:

    except socket.error as msg:
        print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

s.close()
sys.exit()

