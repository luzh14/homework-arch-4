#!/usr/bin/env python
import re,urllib2,sys,os

def get_links(url):
    try:
        result = urllib2.urlopen(url)
    except urllib2.URLError,e:
        if hasattr(e, "code"):
            print "The server couldn't fulfill the request."
            print "Error code: %s" % e.code
        elif hasattr(e, "reason"):
            print "We failed to reach a server. Please check your url and read the Reason"
            print "Reason: %s" % e.reason
        sys.exit(2)
    content = result.read().decode("utf-8")
    print "Read webpage successfully."
    pattern = re.compile(r'\stitle.*img\ssrc="(.*)"\salt="(.*)"/></a>')
    results = re.findall(pattern, content)
    return results

def file_save((url_avatar,username),count):
    dirname = os.path.dirname(sys.argv[0]) 
    dir_imgs = os.path.join(dirname,'imgs')
    if not os.path.exists(dir_imgs):
        os.mkdir(dir_imgs)
    img = urllib2.urlopen(url_avatar)
    filename = dir_imgs+'/'+username+'.jpg'
    if not os.path.exists(filename):
        with open(filename,'w') as f:
            f.write(img.read())
            count+=1
    return count

if __name__ == "__main__":
    count = 0
    page_num = 0 
    while count < 100:
        page_num+=1
        website = "http://www.douban.com/interest/1/1/?p=%d" % (page_num)
        outp = get_links(website)
        outp = list(set(outp))
        l_outp = len(outp)
        for i in xrange(l_outp):
            count = file_save(outp[i],count)
    print "Download %d avatars successfully." % count


