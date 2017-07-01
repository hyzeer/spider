import requests
import re
import random

headers = {'Accept': 'text/html,*/*;q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN',
           'Cache-Control': 'no-cache',
           'Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',}

accounts = {'陈斯湾':['chensiwan','chensiwa'],
            '郑老师':['285669','344848'],
            '官校长':['gjp666','755005'],
            '王老师':['wcy70','888888'],
            '吴卉':['369893197','880701'],
            '符莉莉':['364748486','36474848'],
            '黄欢欢':['199177','19910707'],}


login = 'http://auth.jxjyzy.com/Login.aspx?ReturnUrl=http://auth.jxjyzy.com/EmailAuth.aspx'
userDownResList = 'http://www.jxjyzy.com/User/UserDownResList.aspx'
latestRes = 'http://www.jxjyzy.com/Search/TopNewest.html'
resourceLink = 'http://download.jxjyzy.com/Resource/ResourceDownload.aspx?ID={0}'

def getDownloadsAmount(session):
    historyDownload = session.get(userDownResList).content.decode('gbk')
    pattern = re.compile('[\u4e00-\u9fa5]\s[\u4e00-\u9fa5][\d]*[\u4e00-\u9fa5]<')
    amount = re.sub('\D', '', str(pattern.findall(historyDownload)))
    return amount

def getDownloadSitePOSTData(Id,session):
    downSite = session.get(resourceLink.format(Id)).content.decode()
    pattern = re.compile('value="[\S]*"')
    datas = pattern.findall(downSite)
    datas = [re.sub('value="|"','',x) for x in datas]
    return datas

def run():
    with requests.session() as s:
        s.headers.update()
        site = s.get(latestRes).content.decode('utf-8')
        pattern = re.compile('\/[\d]*.html"\starget')
        resources = pattern.findall(site)
        resources = [re.sub('\D','',x) for x in resources]

    for name,acc in accounts.items():
        with requests.session() as s:
            s.headers.update(headers)
            s.post(login,data={'__VIEWSTATE':'/wEPDwUKMTQ5NjMwOTgwNA9kFgICAQ9kFgQCCQ8WAh4HVmlzaWJsZWhkAhEPDxYCHgRUZXh0BQExZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFCmNoa1NhdmVQd2Q69nxS3CWQ9LAqdh1GdvCYmjRa3A==',
                               '__VIEWSTATEGENERATOR':'C2EE9ABB',
                               '__EVENTVALIDATION':'/wEWBQLMpvPnBQKUj8fhDAK1qbSRCwKigr0xAoLch4YMlzo9XSc3jr6HyJe/XxKGbzHqeZo=',
                               'txtAccount':acc[0],
                               'txtPassword':acc[1],
                               'btnLogin':'登录',})
            beforeDown = getDownloadsAmount(session=s)
            resourceId = resources[random.randint(0,len(resources)-1)]
            datas = getDownloadSitePOSTData(Id=resourceId,session=s)
            s.post(resourceLink.format(resourceId),data={'__VIEWSTATE':datas[0],
                                                         '__VIEWSTATEGENERATOR':datas[1],
                                                         '__EVENTVALIDATION':datas[2],
                                                         'btnDL.x':'68',
                                                         'btnDL.y':'27',})
            afterDown = getDownloadsAmount(session=s)
            print('{}  下载前:{} 下载后:{}'.format(name,beforeDown,afterDown))

if __name__=='__main__':
    run()