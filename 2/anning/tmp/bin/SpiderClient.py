#!/usr/bin/env python
#-*-coding:utf8-*-

""" Spider client """

import zmq, time, random, os
import urllib

pictnum = raw_input('Please enter the image number: ')

class SpiderClient(object):

    """ Spider client handle """

    def __init__(self, Sockfile, pictnum, pictdir):

        self.Sockfile = Sockfile
        self.pictnum = pictnum
        self.pictdir = pictdir

    def downpict(self,urldict):
        usename,urls = urldict.items()[0]
        urllib.urlretrieve(urls,
                           os.path.join(self.pictdir,usename + '.gif'))

        print 'downloading: %s,save: %s.gif .' %(urls,usename)

    def run(self):

        while True:

            context = zmq.Context()
            sockclient = context.socket(zmq.REQ)
            sockclient.connect(self.Sockfile)
            poller = zmq.Poller()
            poller.register(sockclient, zmq.POLLIN)

            sockclient.send_pyobj(int(self.pictnum))

            if poller.poll(60 * 1000):
                UrlList = sockclient.recv_pyobj()
                map(self.downpict,UrlList)
                break

            else:
                sockclient.close()
                context.term()
                print 'Service timeout, try again later!'
                time.sleep(random.randint(1, 5))
                continue

        print 'Task to complete !'

if __name__ == '__main__':

    pictdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    Sockfile = 'tcp://xxx.xxx.xxx.xxx:9999'
    client = SpiderClient(Sockfile,pictnum,pictdir)
    client.run()



