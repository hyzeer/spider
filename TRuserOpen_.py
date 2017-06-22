import requests
import datetime

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

url = 'http://10.73.230.5:1816/'
info = input("请输入资料:")
l = info.split()
usrpsw = l[7].split('/')
l[7] = usrpsw[0]
l.insert(8,usrpsw[1])
timecover = l[9].split("/")
timecover_ = datetime.date(int(timecover[0]),int(timecover[1]),int(timecover[2]))
timecover__ = timecover_
l[9] = timecover__
s = requests.session()
s.headers.update(headers)
s.post(url+'admin/login',data={'username':'admin','password':'root'})
result = s.post(url+'admin/customer/open',data={'node_id':'2',
                                           'realname':'%s'%(l[1]),
                                           'idcard':'0',
                                        'mobile':'%s'%(l[5]),
                                           'email':'0',
                                           'address':'%s'%(l[4]),
                                           'account_number':'%s'%(l[7]),
                                           'password':'%s'%(l[8]),
                                           'ip_address':'',
                                           'product_id':'6',
                                           'months':'0',
                                           'giftdays':'0',
                                           'fee_value':'288.00',
                                           'expire_date':'%s'%(l[9]),
                                           'status':'1',
                                           'customer_desc':'',
                                           'submit':'',}).text
if "alert-warning" not in result:
    print("开户成功")
else:
    print("未知错误,开户失败")
s.close()