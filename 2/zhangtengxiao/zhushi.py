注释

请求头：
GET http://www.zhihu.com/ HTTP/1.1          #get方式请求 知呼网址 使用http1.1 
Host: www.zhihu.com                         #host为get请求的host
Proxy-Connection: keep-alive                #开启会话保持 
Cache-Control: max-age=0                    #缓存最大值是0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8           #浏览器可接受的请求内容 q是协商值
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36            #agent类型
DNT: 1                                                        #希望不允许追踪    Do Not Track  1代表用户不想被第三方网站追踪，0代表接受追踪，null代表用户不置可否。
Accept-Encoding: gzip, deflate, sdch                          #请求头可可接受编码类型
Accept-Language: zh-CN,zh;q=0.8                               #请求头可可接受语言类型 
Cookie: _ga=GA1.2.1504299805.1423378481;                      #cookie用于客户端识别

响应头：
HTTP/1.1 200 OK                                      #http协议 返回状态码
Server: zhihu_nginx                                  #服务器类型
Date: Sun, 19 Apr 2015 11:30:36 GMT                   #返回创建报文的时间
Content-Type: text/html; charset=UTF-8               #返回内容类型和字符集
Vary: Accept-Encoding                                #返回 服务端协商中用到客户端的哪些请求
Content-Security-Policy: default-src *; frame-src *.zhihu.com getpocket.com note.youdao.com; script-src *.zhihu.com *.google-analytics.com zhstatic.zhihu.com 'unsafe-eval'; style-src *.zhihu.com 'unsafe-inline'
                                                     #定义页面可以加载哪些资源
Set-Cookie: r_c=1; Domain=zhihu.com; Path=/          #设置cookie 第一个;前面是cookie名和值 是强制的
Expires: Fri, 02 Jan 2000 00:00:00 GMT               #返回失效的日期和时间与缓存关联
Vary: Accept-Encoding                  
Pragma: no-cache                                     #强制缓存没有过期的情况下重新向服务器进行验证
Cache-Control: private, no-store, max-age=0, no-cache, must-revalidate, post-check=0, pre-check=0  #传输缓存信息
X-Frame-Options: DENY                  #
Content-Encoding: gzip                 #服务器对内容做过哪些类型的编码，客户端通过这信息进行解码。此处用到gzip压缩。
Transfer-Encoding: chunked             #通过编码安全的传送http主体报文 chunked是对报文主体执行过的列表
Connection: keep-alive                 #连接保持
Keep-Alive: timeout=15                 #会话超时时间
