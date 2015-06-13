#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'luke'

import sys, os
import json
import operator

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet
import conf
def ff(d_in):
    ops={'>':operator.gt,'<':operator.lt}
    for cf in conf.ff_conf:
        data = json.loads(d_in)
        current_value=data[cf[0]]
        liminal_value=cf[2]
        opt=cf[1]
        alert_mail=cf[3]
        if (ops[opt](current_value,liminal_value)):
            sendMail(alert_mail)


def sendMail(alert_mail):
    print('sendmail to %s'%alert_mail)

if __name__ == '__main__':
    def logic(d_in):
        print('d_in%s'%d_in)
        print('d_in type%s'%type(d_in))
        ff(d_in)
#        print d_in
        return("OK")

    saverD = nbNet('0.0.0.0', 50138, logic)
    saverD.run()