#!/usr/bin/env python

import socket, sys, os

HOST = '127.0.0.1'
PORT = 9079
CNT = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

cmd = sys.argv[1]
data = "%010d%s"%(len(cmd), cmd)
s.send(data * CNT)
#s.recv(len(data) * CNT)
for i in xrange(CNT):
    buf = s.recv(len(data))
    #print buf
