
请求头：

GET http://www.zhihu.com/ HTTP/1.1  
    # 向服务器发送请求：
    #    请求格式: 请求方法 URI 协议版本
    #    请求方法GET, 浏览器采用GET方法向服务器获取资源；
    #    请求HTTP URL: http://www.zhihu.com/ 如无PATH，默认请求"/"; 
    #       因为使用了代码，所以此处URI是完整域名
    #    HTTP版本为1.1 ，且其后必须增加一个空行，即最后有CRLF(\r\n)

Host: www.zhihu.com
    # 请求Host: www.zhihu.com(CRLF)
    # 用于服务器确定请求的域名，因为一个IP下可能有多个不同的域名

Proxy-Connection: keep-alive
    # 浏览器开启了代理功能, Proxy-Connection 替换了Connection.
    # 所以GET中请求头变成了http://www.zhihu.com/, 否则应该是'GET / HTTP/1.1'; 

Cache-Control: max-age=0
    # 控制网页缓存的，max-age<=0可以等价于no-cache, 
    #    每次访问此网页都会请求服务器以检查是否有更新，而不是直接访问本地缓存304, 
    #    如何max-age=15 就是15秒肉可以直接使用本地缓存，

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    # 表示浏览器支持的MIME类型，媒体类型和内容类型，
    #     '/'前是类型，'/'后是子类型，就是大范围和范围中精确类型, 
    #     */*代表任意类型，q代表优先级
 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
    # 客户端类型（如浏览器，爬虫等），
    # 对于浏览器，空个字段有很多历史因素，导致字段很长

DNT: 1
    # Do Not Track 禁止追踪的简称，
    # 用户选择了这个字段就免于被第三方网站追踪网络痕迹。
    #    1 代表用户不想被第三方网站追踪，0 代表接收，null代表用户无所谓，

Accept-Encoding: gzip, deflate, sdch
    # 客户端浏览器发给服务器，声明浏览器支持的编码类型
    # 如果不写，默认是identity，不过服务器端通常会返回压缩包
    # gzip是最常用的压缩，减少网络传输，deflate也是一种压缩算法
    # sdch是一种新的压缩算法, chrome支持。
    #   通过字典压缩算法对各个页面相同的内容进行压缩，减少相同的内容重复传输

Accept-Language: zh-CN,zh;q=0.8
    # 浏览器支持的语言，优先支持简体中文，q是权重系数范围0=<q<=1

Cookie: _ga=GA1.2.1504299805.1423378481;
    # Cookie信息


响应头：
HTTP/1.1 200 OK
    # HTTP响应头，200系统列表成功。

Server: zhihu_nginx
    # 包含了服务器端用来处理请求的软件信息。

Date: Sun, 19 Apr 2015 11:30:36 GMT
    # 响应消息产生的时间

Content-Type: text/html; charset=UTF-8
    # 返回消息的文档属于什么类型的MIME类型，及字符集，
    #     这样就会通知浏览器如何显示返回的消息内容

Vary: Accept-Encoding
    # 告诉代理服务器缓存两种版本的资源：压缩和非压缩，
    # 有助于避免一些公共代理不能正确的检测Content-Encoding

Content-Security-Policy: default-src *; frame-src *.zhihu.com getpocket.com note.youdao.com; script-src *.zhihu.com *.google-analytics.com zhstatic.zhihu.com 'unsafe-eval'; style-src *.zhihu.com 'unsafe-inline'
    # 与内容安全是有关的，定义页面可以加载哪些资源，减少XSS

Set-Cookie: r_c=1; Domain=zhihu.com; Path=/
    # Cookie和Set-Cookie是2个HTTP头部和cookie相关的参数，
    # Cookie头由客户端（浏览器）发送的，包含在HTTP请求头部。
    # Set-cookie是用于服务器发送给客户端的，包含在响应头部，用于客户端创建一个cookie；
    # 如果没有指定expires,所以当回话关闭Cookie就失效

Expires: Fri, 02 Jan 2000 00:00:00 GMT
    # HTTP控制缓存的基本手段, 时间必须是GMT，而不是本地时间. 还是Cache-Control可以控制更多点

Pragma: no-cache
    # 和Cache-Control一样，只是为了兼容http/1.0, 而Cache-Control兼容1.1

Cache-Control: private, no-store, max-age=0, no-cache, must-revalidate, post-check=0, pre-check=0
    # 缓存控制规则，用于控制请求／响应过程中缓存必须遵守的指令。
    # 默认为private，所有内容只缓存到私有缓存中。
    # no-store表示不缓存

X-Frame-Options: DENY
    # 防止网页被Frame

Content-Encoding: gzip
    # WEB服务器表明自己使用了gzip压缩方法

Transfer-Encoding: chunked
    # 分块传输编码，
    # 通常不使用分块时，待发送数据做为一个整块发送，需要使用Content-Length字段表示长度
    # 使用分块方式时，不需要知道待输出内容的长度，可以使用更少的空间动态的生成要发送的数据。
    # 最后发送一个空块表示结束

Connection: keep-alive
    # 保持会话联接

Keep-Alive: timeout=15
    # 会话超时时间


