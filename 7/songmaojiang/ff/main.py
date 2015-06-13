#!/usr/bin/env python
# coding=utf-8

import sys, os 
import json
import operator

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet

conf_name = './conf.py'

class filter:
    def __init__(self, d_in, conf):
        self.data = json.loads(d_in)
        self.conf = conf

    def print_info(self):
        print("\n+ data:")
        print(json.dumps(self.data, indent=2))
        print("\n+ conf:")
        print(json.dumps(self.conf, indent=2))
            
    def sendEmail(self, info, email):
        print("\t\tsend '%s' to email of: %s" % (info, email))


    def process(self, key):
        ''' compare the current data with conf data'''
        print("\tin process of %s" % key)
        
        # process
        ops = {">": operator.gt, "<": operator.lt}
        confGtlt = self.conf[key][0]
        confData = self.conf[key][1]
        confData = float(confData)

        currData = self.data[key]

        if (ops[confGtlt](currData, confData) ):
            self.sendEmail("%s: big than %d" % (currData, confData), self.conf[key][2])
        else:
            print("\t%s normal" % key)


    def run(self):
        #self.print_info()
        for item in self.conf.iterkeys():
            print("\n-- in run()")
            self.process(item)


if __name__ == '__main__':

    def get_conf():
        '''read conf from file'''
        with file(conf_name) as fr:
            fr_json = json.load(fr)
            #print(json.dumps(fr_json, indent=4))
            if fr_json is None:
                print("conf is none, exit")
                sys.exit(1)
            return fr_json

    def logic(d_in):
        f = filter(d_in, get_conf())
        f.run()
        return("OK")

    saverD = nbNet('0.0.0.0', 50762, logic)
    saverD.run()

