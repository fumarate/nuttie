import requests
from bs4 import BeautifulSoup

import time


class Sign:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.session.headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"}

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
        try:
            url = "https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/mrybtb.jsp"  # 先进一次
            resp = self.session.get(url)
            api_root = "https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/"
            # 可判断是否返校
            HUR = self.session.post(
                api_root + "com.sudytech.work.uust.zxxsmryb.xxsmryb.hdlgUtil.biz.ext").json()["result"]
            if len(HUR) == 0:
                print("没有返校")
                return
            QDR = {}
            QDR = self.session.post(
                api_root + "com.sudytech.work.uust.zxxsmryb.xxsmryb.queryDrsj.biz.ext").json()["result"]
            if "result" in QDR.keys():
                print("已经签到")
            e = Sign.get_entity(HUR[0])
            self.session.post(
                api_root+"com.sudytech.work.uust.zxxsmryb.xxsmryb.saveOrupte.biz.ext", json=e)
            print("签到成功")
        except Exception as e:
            print(e)
            print("签到失败,可能是账号被风控.")

    @staticmethod
    def get_entity(HUR):
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
    a = Sign("YourID", "YourPassword")
    a.login()
    a.sign()
    a.logout()
