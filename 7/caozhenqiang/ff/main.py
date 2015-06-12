#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import  nbNet

def logic(d_in):
    data = json_load(d_in)
    
transD = nbNet('0.0.0.0', 50000, logic)
transD.run()

