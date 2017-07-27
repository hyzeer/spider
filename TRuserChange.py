import requests
import datetime
import re

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

url = 'http://10.73.230.5:1816/'
packages = {'6M':'2','10M':'3','20M':'4','50M':'5','100M':'6','30M':'14','60M':'15'}
s = requests.session()
s.headers.update(headers)
s.post(url+'admin/login',data={'username':'admin','password':'root'})
for line in open(b'D:\\xufei.txt','r'):
    l = line.split()
    timecover = l[4].split("-")
    timecover_ = datetime.date(int(timecover[0]), int(timecover[1]), int(timecover[2]))
    l[4] = str(timecover_ + datetime.timedelta(365))
    if '100M' in l[5]:
        rate = l[5].split('￥')
        l.insert(6, rate[0][-4::])
        l[9] = re.sub('\D', '', l[9])
    if '100M' not in l[5]:
        rate = l[6].split('￥')
        l[6] = rate[0]
        l[9] = re.sub('\D', '', l[9])

    result = s.post(url + 'admin/account/change', data={'account_number': '%s' % (l[13]),
                                                        'product_id': '%s' % (packages[l[6]]),
                                                        'add_value': '%s' % (l[9]),
                                                        'back_value': '0',
                                                        'expire_date': '%s' % (l[4]),
                                                        'balance': '0.00',
                                                        'time_length': '0.00',
                                                        'flow_lengh': '0',
                                                        'operate_desc': '',
                                                        'submit': ''}).text
    if "alert-warning" not in result:
        print("{0} 缴费成功".format(l[13]))
    else:
        print("未知错误,缴费失败")
    s.close()