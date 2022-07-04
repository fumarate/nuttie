import requests
from bs4 import BeautifulSoup

import time
import json
        
def send_mail(mail_config:dict,msg:str,target:str)->None:
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    message = MIMEText(msg.replace("\n","<br/>"), 'plain', 'utf-8')
    message['From'] = Header("✔AutoSign", 'utf-8')
    message['To'] =  Header(str(target), 'utf-8')
    message['Subject'] = Header("健康打卡状态通报", 'utf-8')
    smtpObj = smtplib.SMTP(mail_config['host'],mail_config['port'])
    smtpObj.login(mail_config['address'],mail_config['password'])
    smtpObj.sendmail(mail_config['address'], [target], message.as_string())
    print ("向%s发送邮件通知成功!通知内容:%s"%(target,repr(msg)))
        
class Client:
    def __init__(self, username, password,overwrite_items:dict={}):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.session.headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"}
        self.api_root="https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/"
        self.entity={}
        self.overwrite_items  = overwrite_items
        
    def login(self):
        print(self.username+"开始登录")
        url = "https://sso.ecust.edu.cn/authserver/login"
        resp = self.session.get(url, allow_redirects=False)
        resp = self.session.get(url, allow_redirects=False)
        data = {}
        data['username'] = str(self.username)
        data['password'] = str(self.password)
        data['captchaResponse'] = ""
        bs = BeautifulSoup(resp.text, "html.parser")
        hidden_items = bs.select("input[type='hidden']")
        for hi in hidden_items:
            data[hi['name']] = hi['value']
        if self.needCaptcha():
            return {
                "status":False,
                "message":"需要验证码！"
            }
        resp = self.session.post(url, data=data)
        # todo 设计登录失败检测
        print(self.username+"登陆成功")
        return{
            "status":True
        }

    def Client(self)->dict:
        """Client

        Returns:
            dict: a dict which contains the information about this Clienting
        """
        print(self.username+"开始打卡")
        try:
            url = "https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/mrybtb.jsp"  # 先进一次
            resp = self.session.get(url)
            api_root = "https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/"
            if not self.queryXsfxry():
                return{
                    "status":False,
                    "message":"该账号无法打卡,请手动检查!"
                }
            if not self.queryDrsj():
                self.session.post(
                    api_root+"com.sudytech.work.uust.zxxsmryb.xxsmryb.saveOrupte.biz.ext", json=self.entity)
                return{
                    "status":True,
                    "message":'打卡成功!'
                }
            else:
                return{
                    "status":True,
                    "message":'该账号今日已经打卡!'
                }
                
        except Exception as e:
            return{
                    "status":False,
                    "message":"程序运行出错!\n报错信息:"+str(e)
                }

    def logout(self):
        url = "https://sso.ecust.edu.cn/authserver/logout?service=/authserver/login"
        self.session.get(url)
    
    def queryXsfxry(self)->bool:
        """_summary_

        Returns:
            bool: if the user is allowed to Client
        """
        resp = self.session.post(self.api_root+"com.sudytech.work.uust.zxxsmryb.xxsmryb.hdlgUtil.biz.ext").json()
        list = resp['result']
        if list is not None and len(list)>0:
            if 'SS' in list[0] and list[0]['SS'] not in [None,'']:
                SS = list[0]['SS']
                list[0]['xq'] =  SS.split("-")[0]
                list[0]['ss'] =  SS.split("-")[1]
                list[0]['mph'] =  SS.split("-")[2]
                list[0].pop('SS')
                self.entity = list[0]
                self.entity.update(self.overwrite_items)
                return True
        return False
    
    def queryDrsj(self):
        """_summary_
        Check if the user has Cliented.
        """
        resp = self.session.post(self.api_root+"com.sudytech.work.uust.zxxsmryb.xxsmryb.queryDrsj.biz.ext").json()
        if 'list' in resp['result'] and resp.json()['result']['list']!={}:
            return False
        return True
    
    def needCaptcha(self):
        resp = self.session.get("https://sso.ecust.edu.cn/authserver/needCaptcha.html?username=%s&_=%d"%(self.username,time.time()))
        return 'true' in resp.text
    def run(self):
        msg = self.login()
        if not msg['status']:
            return msg
        msg = self.Client()
        self.logout()
        return msg

if __name__ == "__main__":
    with open("config.json",mode="r+",encoding='utf-8') as config_file:
        config_json = json.load(config_file)
        config_public = config_json['public']
        msgs = []
        for user in config_json['users']:
            client = Client(user['username'],user['password'],user['overwrite_items'])
            result_msg = client.run()
            result_msg['username'] = user['username']
            msgs.append(result_msg)
            for report in user['report']:
                if report['method'] == 'mail':
                    send_mail(config_public['sender'],result_msg['username']+result_msg['message'],report['mail'])
        send_mail(config_public['sender'],time.strftime("%Y/%m/%d %H:%M:%S")+'\n'+'\n'.join(list(map(lambda m:m['username']+m['message'],msgs))),config_public['receiver']['mail'])
    
