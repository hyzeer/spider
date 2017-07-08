import requests
import re

headers = {'Accept': 'text/html,*/*;q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN',
           'Cache-Control': 'no-cache',
           'Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',}

account = {'user.userLogin':'362524199107073529','user.userPwd':'073529','remenber':'1'}
#Id = {'pc':'1','studentinfo.idCardNo':'361023200706102513'}

login_in = 'http://wsfwj3.jxedu.gov.cn/HomeVisits/system/loginAction!loginIn.action'
Id_submit = 'http://wsfwj3.jxedu.gov.cn/HomeVisits/teacherManage/homeVisitInfoAction!saveStudent.action'
info_submit = 'http://wsfwj3.jxedu.gov.cn/HomeVisits/teacherManage/homeVisitInfoAction!saveStudentInfo.action'
def formatStudentInfo(htmlInfo,id):
    pattern = re.compile('name="[\w]*"\svalue="[\w\S]*"')
    pre_data = pattern.findall(htmlInfo)
    if pre_data != []:
        datalist = [str(re.sub('"|name=|value=','',x)).split() for x in pre_data]
        datalist[-2].append('')
        datalist.append(['familyType','0'])
        datadic = {key:value for key,value in datalist}
        return datadic
    if pre_data == []:
        print(html)
        print(id)

with open('D:\\studentId.txt','r') as f:
    for line in f:
        Id = {'pc': '1', 'studentinfo.idCardNo': line}
        with requests.session() as s:
            s.headers.update(headers)
            s.post(login_in,data=account)
            html = s.post(Id_submit,data=Id).content.decode('utf-8')
            data = formatStudentInfo(html,line)
            s.post(info_submit,data=data)
            print(data)

