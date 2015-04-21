#!/usr/bin/env python
#-*-coding:utf8-*-

""" Spider Serve """

import zmq, os, sys, itertools
import requests, re

__requires__ = ['daemon']

try:
    import pkg_resources
except Exception:
    pass

local_module_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'lib')
)
sys.path.append(local_module_path)

from daemon import Daemon

class SpiderHandle(Daemon):

    ''' Multi user Spider handle '''

    def __MatchingHandle(self, text):

        result = re.match(r'.*\W+<img src="(?P<urls>.+)" class.+alt="(?P<usename>.+)"/>',
                          text)

        usename = result.group('usename')
        urls = result.group('urls')
        return usename,urls

    def StringOperation(self,Pictnum):

        UrlList=[]

        for page in itertools.count():
            if not page % 35:
                payload = {'start': page}
                r = requests.get(self.Urlsite,
                                params=payload)

                if r.ok:
                    html = r.text
                    TextList = html.split('<li class="">\n        <div class="pic">\n        ')[1:]
                    [UrlList.append({usename:urls}) for usename, urls in itertools.imap(self.__MatchingHandle,TextList)]

                    if len(UrlList) >= Pictnum:
                        break

        return UrlList

    def _run(self, ):

        context = zmq.Context()
        Serversocks = context.socket(zmq.REP)
        Serversocks.bind(self.Sockfile)
        poller = zmq.Poller()
        poller.register(Serversocks, zmq.POLLIN)

        while True:

            events = dict(poller.poll())

            if Serversocks in events and events[Serversocks] == zmq.POLLIN:
                Pictnum = Serversocks.recv_pyobj()
                UrlList = self.StringOperation(Pictnum)

                Serversocks.send_pyobj(UrlList)

if __name__ == '__main__':

    Sockfile = "tcp://xxx.xxx.xxx.xxx:9999"
    Urlsite = 'http://www.douban.com/group/151187/members'

    Pidfile = os.path.join(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'tmp')
        ),'master.pid')

    spider = SpiderHandle(Pidfile, Sockfile, Urlsite)

    if len(sys.argv) == 2:

        if 'start' == sys.argv[1]:
            spider.start()

        elif 'stop' == sys.argv[1]:
            spider.stop()

        elif 'restart' == sys.argv[1]:
            spider.restart()

        else:
            print "Unknown command"
            sys.exit(2)

        sys.exit(0)

    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

