import requests
import datetime
import sys

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

url = 'http://10.73.230.5:1816/'
packages = {'6M':'2','10M':'3','20M':'4','50M':'5','100M':'6'}
l = sys.argv
timecover = l[8].split("/")
timecover_ = datetime.date(int(timecover[0]),int(timecover[1]),int(timecover[2]))
timecover__ = timecover_
l[8] = timecover__
s = requests.session()
s.headers.update(headers)
s.post(url+'admin/login',data={'username':'admin','password':'root'})
result = s.post(url+'admin/customer/open',data={'node_id':'2',
                                           'realname':'%s'%(l[1]),
                                           'idcard':'0',
                                        'mobile':'%s'%(l[2]),
                                           'email':'0',
                                           'address':'%s'%(l[3]),
                                           'account_number':'%s'%(l[4]),
                                           'password':'%s'%(l[5]),
                                           'ip_address':'',
                                           'product_id':'%s'%(packages[l[6]]),
                                           'months':'0',
                                           'giftdays':'0',
                                           'fee_value':'%s.00'%(l[7]),
                                           'expire_date':'%s'%(l[8]),
                                           'status':'1',
                                           'customer_desc':'',
                                           'submit':'',}).text
if "alert-warning" not in result:
    print("开户成功")
else:
    print("未知错误,开户失败")
s.close()


#参数格式:姓名 电话 地址 账号 密码 速率 价格 到期时间