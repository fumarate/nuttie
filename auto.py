import requests
from bs4 import BeautifulSoup

import time


class Sign:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def login(self):
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
        resp = self.session.post(url, data=data)

    def sign(self):
        url = "https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/mrybtb.jsp"  # 先进一次
        resp = self.session.get(url)
        api_root = "https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/"
        # 可判断是否返校
        HUR = self.session.post(
            api_root + "com.sudytech.work.uust.zxxsmryb.xxsmryb.hdlgUtil.biz.ext").json()["result"]
        if len(HUR) == 0:
            print("没有返校")
            return
        QDR = self.session.post(
            api_root + "com.sudytech.work.uust.zxxsmryb.xxsmryb.queryDrsj.biz.ext").json()["result"]
        e = Sign.get_entity(HUR, QDR)
        res = self.session.post(
            api_root+"com.sudytech.work.uust.zxxsmryb.xxsmryb.saveOrupte.biz.ext", json=e)

    @staticmethod
    def get_entity(HUR, QDR):
        entity = {
            "entity": {
                "ryid": HUR['RYID'],
                "xm": HUR['XM'],
                "xh": HUR['XH'],
                "xydm": HUR['XYDM'],
                "xy": HUR['XY'],
                "bj": HUR['BJ'],
                "xb": HUR['XB'],
                "lxdh": HUR['LXDH'],
                "rysf": HUR['RYSF'],
                "xq": (xsm := HUR['SS'].split("-")[0]),
                "ss": HUR['SS'],
                "mph": xsm[2],
                "sfzh": HUR['SFZH'],
                "jtzz": HUR['JTZZ'],
                "jjlxr": HUR['JJLXR'],
                "jjlxrdh": HUR['JJLXRDH'],
                "fdygh": HUR['FDYGH'],
                "fdy": HUR['FDY'],
                "swjkzk": "健康",  # sw健康状况,
                "xcm": "是",  # 行程码
                "jkmtp": "",
                "xcmtp": "",
                "hsjcbgtp": "",
                "twsfzc": "是",  # 体温是否正常
                "swdqtw": "",
                "swbz": "",
                "jkmsflm": "是",  # 健康码是否绿码
                "sfycxxwc": "否",  # 是否有从学校外出
                "tUustMrybhdgjs": "[]",
                "_ext": "{\"jkmtp\":{\"type\":\"fileUpload\",\"value\":[],\"nameStyle\":\"\"},\"xcmtp\":{\"type\":\"fileUpload\",\"value\":[],\"nameStyle\":\"\"},\"hsjcbgtp\":{\"type\":\"fileUpload\",\"value\":[],\"nameStyle\":\"\"}}",
                "tjsj": time.strftime("%Y-%m-%d %H:%M"),
                "tjrq": time.strftime("%Y-%m-%d"),
                "zb": "[]",
                "__type": "sdo:com.sudytech.work.uust.zxxsmryb.zxxsmryb.TUustZxxsmryb"
            }
        }
        return entity

    def logout(self):
        url = "https://sso.ecust.edu.cn/authserver/logout?service=/authserver/login"
        self.session.get(url)


if __name__ == "__main__":
    a = Sign("YourUserId", "YourPassword")
    a.login()
    a.sign()
    a.logout()
