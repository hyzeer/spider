import requests
import IPy
import re
import threading

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

ips = IPy.IP('10.190.196.0/23')
ip_1 = ips[1:65]
ip_2 = ips[65:129]
ip_3 = ips[129:193]
ip_4 = ips[193:257]
ip_5 = ips[257:321]
ip_6 = ips[321:385]
ip_7 = ips[385:449]
ip_8 = ips[449:511]
online={'1':'在线','2':'离线'}
modem = input('请输入终端SN(不输入默认为遍历所有局端中未添加备注的终端):')
if modem != '':
    modem = re.sub(':','',modem)
    modem = list(modem)
    modem.insert(2,':')
    modem.insert(5,':')
    modem.insert(8,':')
    modem.insert(11,':')
    modem.insert(14,':')
    modem = str(modem)
    modem = re.sub("[',\[\]\s]",'',modem)
def run(modem,ips):
    for ip in ips:
        try:
         url = 'http://' + str(ip)
         s = requests.session()
         s.headers.update(headers)
         s.post(url+'/goform/command',data={'CMD':'LOGIN','uname':'admin','pws':'cvn'},timeout=0.2)
         result = s.get(url+'/netTopology.asp').content.decode('gbk')
         if s.get(url + '/netTopology.asp').status_code == 404:
             otec(modem,ip)
             continue
         s.close()
         if modem == '':
            pattern = re.compile("'[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]','[0-9]','[0-9]','[0-9]*-[0-9]*-[0-9]*-[0-9]*-','[A-Z0-9-]*','\d*','\d*','\d*','\d*','[A-Z0-9]*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]'")
         if modem != '':
            pattern = re.compile("'%s','[0-9]','[0-9]','[\S\s]*?','[A-Z0-9-]*','\d*','\d*','\d*','\d*','[A-Z0-9]*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','[\S\s]*?'"%(modem))
         r = pattern.findall(result)
         if(len(r) > 0):
             r = re.sub("'", '', r[0]).split(',')
             time = re.sub('\D', ' ', r[3]).split()
             print(url + " MAC地址:%s  用户名:%s  状态:%s  上下线时间:%s天%s小时%s分%s秒  设备类型:%s  上行/下行带宽:%s/%s  衰减:%s  SNR:%s" % (r[0], r[19], online[r[1]], time[0], time[1], time[2], time[3], r[9], r[18], r[5], r[6], r[7]))

        except UnicodeDecodeError:
         result = s.get(url + '/netTopology.asp').content.decode('utf-8')
         s.close()

         if modem == '':
             pattern = re.compile("'[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]','[0-9]','[0-9]','[0-9]*-[0-9]*-[0-9]*-[0-9]*-','[A-Z0-9-]*','\d*','\d*','\d*','\d*','[A-Z0-9]*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]'")
         if modem != '':
            pattern = re.compile("'%s','[0-9]','[0-9]','[\S\s]*?','[A-Z0-9-]*','\d*','\d*','\d*','\d*','[A-Z0-9]*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','[\S\s]*?'"%(modem))
         r = pattern.findall(result)
         if (len(r) > 0):
             r = re.sub("'",'',r[0]).split(',')
             time = re.sub('\D',' ',r[3]).split()
             print(url + " MAC地址:%s  用户名:%s  状态:%s  上下线时间:%s天%s小时%s分%s秒  设备类型:%s  上行/下行带宽:%s/%s  衰减:%s  SNR:%s" % (r[0],r[19],online[r[1]], time[0], time[1], time[2], time[3], r[9], r[18], r[5], r[6], r[7]))
         continue

        except Exception:
         continue

def otec(modem,ip):
    url = 'http://' + str(ip)
    s = requests.session()
    s.headers.update(headers)
    s.get(url + '/goform/webs_login?cmd=set&username=admin&password=admin', timeout=0.2)
    result = s.get(url + '/goform/webs_online_hmd_list?Mas_Id=100').content.decode('gbk')
    s.close()

    if modem == '':
        pattern = re.compile(r'<td align="center" style="font-size:13px"></td>')
        r = pattern.findall(result)
        if (len(r) > 0):
            print(url + '有 %s 台终端未添加用户信息' % (len(r)))
    if modem != '':
        pattern = re.compile(modem.lower())
        r = pattern.findall(result)
        r = set(r)
        if (len(r) > 0):
            print(url + str(r))


threads = []
t1 = threading.Thread(target=run,args=(modem,ip_1))
t2 = threading.Thread(target=run,args=(modem,ip_2))
t3 = threading.Thread(target=run,args=(modem,ip_3))
t4 = threading.Thread(target=run,args=(modem,ip_4))
t5 = threading.Thread(target=run,args=(modem,ip_5))
t6 = threading.Thread(target=run,args=(modem,ip_6))
t7 = threading.Thread(target=run,args=(modem,ip_7))
t8 = threading.Thread(target=run,args=(modem,ip_8))
threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)
threads.append(t5)
threads.append(t6)
threads.append(t7)
threads.append(t8)

for t in threads:
  #t.setDaemon(True)
  t.start()

t.join()