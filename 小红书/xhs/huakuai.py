import random
import re

import requests

import execjs
from getimg import Img
from track import Track
from orgaction import get_gap
import time
from loguru import logger
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 忽略特定类型的警告
warnings.filterwarnings("ignore", message="urllib3 (1.26.14) or chardet (5.2.0)/charset_normalizer (2.0.12) doesn't match a supported version!", category=InsecureRequestWarning)

timstr = str(time.time()*1000)

with open(r'trackencrypt.js','r',encoding='utf-8') as fp:
    jsstr = fp.read()
class Xhs_Slider:
    def __init__(self):
        self.headers =  headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": "https://servicewechat.com/wxb296433268a1c654/108/page-frame.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8447",
        # "X-WECHAT-HOSTSIGN": "{\"noncestr\":\"44729805311ed2cd0ac08f8b4cac5114\",\"timestamp\":1711421951,\"signature\":\"951d684dea7e703dc4970950fa15650f988c0eb3\"}",
        "xweb_xhr": "1"
    }
        self.jsstr = jsstr
        self.ctx = execjs.compile(jsstr)
        self.url = 'https://captcha.fengkongcloud.com/ca/v1/fverify'
        self.parms = Img()


    def get_enc_track_data_and_rid(self):
        bg_conent,fg_content,key,l,rid = self.parms.getparms()
        distance = get_gap(bg_conent,fg_content)
        logger.info(f"滑动距离{distance}")
        track_list = Track.get_slice_track(target_point=int(distance * 372 / 600))
        logger.info(f'轨迹==>{track_list}')
        req_data = {
            "d": int(distance * 372 / 600) / 372,
            "m": track_list,
            "c": track_list[-1][2] + random.randint(20, 100),
            "w": 372,
            "h": 186,
            "os": "weapp",
            "cs": 0,
            "wd": 0,
            "sm": 1
        }
        enc_track_data = self.ctx.call("getMouseAction", req_data, key, l)
        logger.info(f"加密轨迹数据:{enc_track_data}")
        return enc_track_data,rid
    def req_data(self):
        track_data,rid = self.get_enc_track_data_and_rid()


        params = {
            "organization": "xxxxxxxx",  # 每个微信不一样
            "appId": "default",
            "channel": "miniProgram",
            "lang": "zh-cn",
            "rversion": "1.0.1",
            "sdkver": "1.3.3",
            "rid": rid,
            "act": track_data,
            "ostype": "weapp",
            "data": "{}",
            "callback": "sm_" + timstr
        }
        response = requests.get(self.url, headers=self.headers, params=params)
        return response

    def slide_verify(self):

        # logger.info(self.req_data().text)
        resp = re.findall(r'"riskLevel":"(.*?)"', self.req_data().text)
        if len(resp) > 0 and resp[0] == 'PASS':
            logger.success("验证通过")
            return 1
        else:
            logger.error("验证失败")
            return 0





if __name__ == '__main__':
    xhs_silde = Xhs_Slider()
    xhs_silde.slide_verify()
    # total = 10
    # count = 0
    # for i in range(1,11):
    #     result = getverfiy()
    #     if result == 1:
    #         count +=1
    # logger.info(f"成功率==>{round(count/total,2)}")
