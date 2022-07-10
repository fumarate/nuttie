from typing import Dict, List
from jinja2 import Template
import requests
import time
MD = 'md'
HTML = 'html'
TITLE = '健康打卡状态通报'


class Reporter:
    def __init__(self, config):
        self.config = config

    def report_admin(self, msg_list: List[Dict]):
        # mail
        if 'mail' in self.config:
            self.send_mail(self.config['mail'], msg_list)
        # serverchan
        if 'sc_key' in self.config:
            requests.get('https://sctapi.ftqq.com/%s.send' % self.config['sc_key'], params={
                'title': TITLE,
                'desp': self.render(msg_list, MD)
            })
            print('发送ServerChan通知成功！')
        # dingtalkbot

    def report(self, mail: str, msg: dict):
        self.send_mail(mail, [msg])

    def send_mail(self, target: str, msg_list: List[Dict]) -> None:
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        message = self.render(msg_list, HTML)
        mail_config = self.config['sender']
        message_mime = MIMEText(message.replace("\n", ""), 'plain', 'utf-8')
        message_mime['From'] = Header("✔AutoSign", 'utf-8')
        message_mime['To'] = Header(str(target), 'utf-8')
        message_mime['Subject'] = Header(TITLE, 'utf-8')
        smtpObj = smtplib.SMTP(mail_config['host'], mail_config['port'])
        smtpObj.login(mail_config['address'], mail_config['password'])
        smtpObj.sendmail(mail_config['address'], [
                         target], message_mime.as_string())
        print("向%s发送邮件通知成功!通知内容:%s" % (target, repr(message)[:40]+"..."))

    def render(self, msg_list: List[Dict], type: str) -> str:
        template = Template('')
        try:
            with open('template/template.%s' % type, mode='r+', encoding='utf-8') as template_file:
                template = Template(template_file.read())
        except FileNotFoundError as e:
            print("retypr your type")
        return template.render(msg_list=msg_list, title=time.strftime("%Y/%m/%d %H:%M:%S"))
