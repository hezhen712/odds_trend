# 导入模块 urllib2
import urllib2

header = {'Host': 'scholar.google.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'}

query = 'i am master'
seedurl = 'http://www.baidu.com'
req = urllib2.Request(seedurl,headers = header)
con = urllib2.urlopen(req)
doc = con.read()
con.close()

file = open('c:\webdata.txt','a')
file = file.write(doc)

