
from optparse import OptionParser

import sys,os,urllib,urllib2,json,re

def CHECK_ARGV():
    m_argv = {}
    usage = "usage: %prog [options] arg1 arg2" 
    parser = OptionParser(usage=usage,version="%prog 1.0")
    parser.add_option("-w","--url",dest="url",
           help=" url. like http://www.me.com",metavar="WEBURL")
    parser.add_option("-t","--top",dest="topmeizi",
            help="show the top of dbmeizi,default use page options",metavar="TOPMEIZI")
    parser.add_option("-p","--page",dest="page",default="1-3",
            help="dbmeizi page you can like --page=4 or --page=1-3,default --page=1-3",metavar="PAGE")
    (options,args) = parser.parse_args()
    len_argv=len(sys.argv[1:])
    if len_argv == 0 :
        print parser.print_help()
        parser.exit(1)
    m_argv=str(parser.values)
    exec("m_argv="+m_argv)
    return m_argv

def ANALYZE_OPTIONS():
    sp='-'
    m_argv=CHECK_ARGV()
    try:
        url=m_argv['url']
        result = urllib2.urlopen(url)
    except urllib2.URLError,e:
        print "error"
    if sp in m_argv['page']:
        page_all=m_argv['page'].split(sp)
        page=xrange(int(page_all[0]),int(page_all[1])+1)
        m_argv['page']=page
        return m_argv
    else:
        page=m_argv['page']
        m_argv['page']=page
        return m_argv


def PAGE_D(url,page):
    page=str(int(page)-1)
    url=url+'?p='+page
    print url
    result=urllib2.urlopen(url)
    content=result.read().decode("utf-8")
    print "Read webpag successfull"
    pattern=re.compile(r'<img class.*>')
    re_all=re.findall(pattern,content)
    return re_all
    
    

def PDBMZ():
    m_argv=ANALYZE_OPTIONS()
    print m_argv
    url=m_argv['url']
    page=m_argv['page']
    if m_argv['topmeizi']:
        now_top=0
        end_top=m_argv['topmeizi']
        s_top=int(end_top)
    else:
        now_top=0
        s_top=0
        end_top=0
    if type(page) == str:
            re_all=PAGE_D(url,page)
            SAVE_TITL_JPG(re_all,now_top,s_top,end_top)
    else:
        for i in page:
            re_all=PAGE_D(url,i)
            top_list=SAVE_TITL_JPG(re_all,now_top,s_top,end_top)
            now_top=top_list[0]
            s_top=top_list[1]
            print now_top,'jieshutop'

def SAVE_TITL_JPG(re_all,now_top,s_top,end_top):
    top_list=[]
    now_top=now_top
    s_top=s_top
    end_top=end_top
    print 'haiyou stop:'+str(s_top)+' 3'
    page_index='mz_page.index'
    pic_urlbase="http://pic.dbmeizi.com"
    dirname='/home/liran/liran/myproject/ireboot/tmp'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for i in re_all:
        title=re.findall(r'data-title="(.*?)"',i)[0]
        title_str=title.encode('utf-8')
        jpg=re.findall(r'data-src="(.*?)"',i)[0]
        jpg_str=jpg.encode('utf-8')
        group=re.findall(r'data-userurl="(.*?)"',i)[0].split("/")[-2]
        group_str=group.encode('utf-8')
        data_url=re.findall(r'data-url="(.*?)"',i)[0]
        data_url=data_url.encode('utf-8')
        if  s_top>0:
            now_top=now_top+1
            s_top=s_top-1
            print title
            with open(dirname+'/'+str(now_top)+'_'+group+"_"+"_"+title,'w') as f:
                f.write(jpg+'\n'+pic_urlbase+data_url+'\n')
            with open(page_index,'a') as f:
                f.write(str(now_top)+'_'+group_str+"_"+"_"+title_str+":    "+pic_urlbase+data_url+"    "+jpg_str+'\n')
            print 'ntop:  '+str(now_top)
        else:
            break
    s_top=int(end_top)-now_top        
    if s_top>0:
        print 'ntop:'+str(now_top)+' 1'
        print 'stop:'+str(s_top)+' 2'
        tmp=now_top,s_top
        top_list=list(tmp)
        return top_list
    else:
        top_list=[0,0]
        return top_list

    





    



if __name__ == '__main__':
    PDBMZ()
