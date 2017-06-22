import requests,IPy,re,threading,time
from itertools import zip_longest

class Spider(threading.Thread):
    def __init__(self,modem,subnet):
        threading.Thread.__init__(self)
        self.modem = modem
        self.subnet = subnet
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, compress',
                   'Accept-Language': 'en-us;q=0.5,en;q=0.3',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    def cvn(self,ip,decode):
        state = {'1': '在线', '2': '离线'}
        url = 'http://' + str(ip)
        with requests.session() as s:
            s.headers.update(self.headers)
            s.post(url + '/goform/command', data={'CMD': 'LOGIN', 'uname': 'admin', 'pws': 'cvn'}, timeout=0.2)
            result,if404 = s.get(url + '/netTopology.asp').content.decode(decode),s.get(url + '/netTopology.asp').raise_for_status()
        if self.modem == '':
           pattern = re.compile("'[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]','[0-9]','[0-9]','[0-9]*-[0-9]*-[0-9]*-[0-9]*-','[A-Z0-9-]*','\d*','\d*','\d*','\d*','[A-Z0-9]*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]'")
        if self.modem != '':
           pattern = re.compile("'%s','[0-9]','[0-9]','[\S\s]*?','[A-Z0-9-]*','\d*','\d*','\d*','\d*','[A-Z0-9]*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','\d*','[\S\s]*?'"%(self.modem))
        r = pattern.findall(result)
        if(len(r) > 0):
           r = re.sub("'", '', r[0]).split(',')
           time = re.sub('\D', ' ', r[3]).split()
           print(url + " MAC地址:%s  用户名:%s  状态:%s  上下线时间:%s天%s小时%s分%s秒  设备类型:%s  上行/下行带宽:%s/%s  衰减:%s  SNR:%s" % (r[0], r[19], state[r[1]], time[0], time[1], time[2], time[3], r[9], r[18], r[5], r[6], r[7]))

    def otec(self,ip,decode='gbk'):
        url = 'http://' + str(ip)
        with requests.session() as s:
            s.headers.update(self.headers)
            s.get(url + '/goform/webs_login?cmd=set&username=admin&password=admin', timeout=0.2)
            result = s.get(url + '/goform/webs_online_hmd_list?Mas_Id=100').content.decode(decode)
        if self.modem == '':
            pattern = re.compile(r'<td align="center" style="font-size:13px"></td>')
            r = pattern.findall(result)
            if (len(r) > 0):
                print(url + '有 %s 台终端未添加用户信息' % (len(r)))
        if self.modem != '':
            pattern = re.compile(self.modem.lower())
            r = pattern.findall(result)
            r = set(r)
            if (len(r) > 0):
                print(url + str(r))

    def run(self):
        for ip in self.subnet:
            try:
                self.cvn(ip,'gbk')
            except UnicodeDecodeError:
                self.cvn(ip, 'utf-8')
                continue
            except requests.exceptions.HTTPError:
                self.otec(ip)
                continue
            except Exception:
                continue

class CreatSpider:
    def __init__(self,modem,network,threadCount):
        self.modem = modem
        if modem != '':
            self.modem = [x for x in modem if x != ':']
            for i in range(2,15,3):
                self.modem.insert(i,':')
            self.modem = str(self.modem)
            self.modem = re.sub("[',\[\]\s]",'',self.modem)
        eachSegmentCount = IPy.IP(network).len() // threadCount
        segment = lambda seq, n: zip_longest(*[iter(seq)] * n)
        self.network = list(segment([x.strNormal(0) for x in IPy.IP(network)], eachSegmentCount))
        self.creat()

    def creat(self):
        for i in self.network:
            Spider(self.modem,i).start()
        time.sleep(2)
        print("ok")

if __name__ == '__main__':
    modem = input('请输入终端SN(不输入默认为遍历所有局端中未添加备注的终端):')
    CreatSpider(modem,'10.190.196.0/23',8)