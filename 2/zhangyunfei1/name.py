#!/usr/bin/env python
import re,urllib2,sys,os

def get_links(url):
    result = urllib2.urlopen(url)
    content = result.read().decode("utf-8")
    print "Read webpage successfully."
    pattern = re.compile(r'\stitle.*img\ssrc="(.*)"\salt="(.*)"/></a>')
    results = re.findall(pattern, content)
    print results
    return results

def file_save((url_avatar,username),count):
    dirname = os.path.dirname(sys.argv[0]) 
    dir_imgs = os.path.join(dirname,'zyfei')
    print dir_imgs
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
    while count < 3:
        page_num+=1
        urls = "http://www.douban.com/?p=%d" % (page_num)
        print urls
        outp = get_links(urls)
        outp = list(set(outp))
        l_outp = len(outp)
        for i in xrange(l_outp):
            count = file_save(outp[i],count)
    print "Download %d page successfully." % count
