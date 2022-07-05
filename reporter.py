from typing import Dict, List
from jinja2 import Template
MD = 'md'
HTML = 'html'


class Reporter:
    def __init__(self):
        pass

    def send_mail(self, mail_config: dict, msg_list: List[Dict], target: str) -> None:
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        message = self.render(msg_list,HTML)
        message_mime = MIMEText(message.replace("\n", "<br/>"), 'plain', 'utf-8')
        message_mime['From'] = Header("✔AutoSign", 'utf-8')
        message_mime['To'] = Header(str(target), 'utf-8')
        message_mime['Subject'] = Header("健康打卡状态通报", 'utf-8')
        smtpObj = smtplib.SMTP(mail_config['host'], mail_config['port'])
        smtpObj.login(mail_config['address'], mail_config['password'])
        smtpObj.sendmail(mail_config['address'], [target], message_mime.as_string())
        print("向%s发送邮件通知成功!通知内容:%s" % (target, repr(message)[:40]+"..."))

    def send_sc(self,msg_list: List[Dict], target: str):
        pass

    def render(self,msg_list: List[Dict], type: str) -> str:
        template = Template('')
        try:
            with open('template/template.%s' % type, mode='r+',encoding='utf-8') as template_file:
                template = Template(template_file.read().replace('\n',''))
        except FileNotFoundError as e:
            print("retypr your type")
        return template.render(msg_list=msg_list)
