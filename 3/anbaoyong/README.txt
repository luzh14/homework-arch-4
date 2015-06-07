download.py是多线程，多fd下载，没有使用线程锁
download_qq.py是多线程，单fd下载，fd使用线程锁
使用方法：
python download.py/download_qq.py  下载地址  线程数
