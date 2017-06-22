import requests

headers = {'Accept': 'text/html,*/*;q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN',
           'Cache-Control': 'no-cache',
           'Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
           'Referer' : 'http://12.12.168.20:9001/rtcrm-clientweb-standard/npage/obim/staff/loginmng/initLogin.do'}

url = 'http://12.12.168.20:9001'
s = requests.session()
s.headers.update(headers)
s.post(url+'/rtcrm-clientweb-standard/npage/obim/staff/loginmng/syslogin.do',data={'systemUserCode':'fg0012','password':'nfgd2017','valid':'Y'})
for line in open(b'D:\\acc.txt','r'):
     s.post(url+'/rtcrm-clientweb-standard//npage/audit/query/fd007/getBroadNo.do',data={'broadBandNo':line})
     print(line + s.post(url+'/rtcrm-clientweb-standard//npage/audit/query/fd007/offerLine.do',data={'broadBandNo':line}).text)