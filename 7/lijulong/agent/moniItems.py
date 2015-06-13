#!/usr/bin/env python
import inspect,commands
import os,time,socket

class mon:
    def __init__(self):
        self.data = {}

    def getLoadAvg(self):
        with open('/proc/loadavg') as load_open:
            a = load_open.read().split()[:3]
            #return "%s %s %s" % (a[0],a[1],a[2])
            return   float('%0.2f'%float(a[0]))
    
    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1])
            return a / 1024

    def getStatsdCPUUse(self):
        cpuinfo = commands.getstatusoutput("ps aux | grep statsd | grep -v 'grep' | awk '{print $3,$11}'")
        if cpuinfo[0] == 0:
            cpuEveryStatsd = cpuinfo[1].split('\n')
            returninfo = None
            for everyStatsd in cpuEveryStatsd:
                cpuUse = everyStatsd.split(" ")[0]
                statsdNUM = everyStatsd.split(" ")[1]
                #print portinfo,uidinfo
                if returninfo == None:
                    returninfo = "%s:%s"%(statsdNUM,cpuUse)
                else:
                    returninfo = "%s,%s:%s"%(returninfo,statsdNUM,cpuUse)
            return returninfo
        else:
            return "Can not get info"

    
    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1]) #Total
                F = int(mem_open.readline().split()[1]) #Free
                B = int(mem_open.readline().split()[1]) #Buffer
                C = int(mem_open.readline().split()[1]) #Cache
                return (T-F-B-C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a / 1024
    
    def getMemFree(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (F+B+C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                mem_open.readline()
                a = int(mem_open.readline().split()[1])
                return a / 1024
    
    def getHost(self):
        return socket.gethostbyname().replace('.','_')
    def getTime(self):
        return int(time.time())
    def runAllGet(self):
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0][:3] == 'get':
                self.data[fun[0][3:]] = fun[1]()
        return self.data

if __name__ == "__main__":
    print mon().runAllGet()
