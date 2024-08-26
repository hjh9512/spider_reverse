import json
import time

import requests

import cv2
import numpy as np
from loguru import logger
import re

timstr = str(time.time() * 1000)


class Img:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Referer": "https://servicewechat.com/wxb296433268a1c654/108/page-frame.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8447",
            # "X-WECHAT-HOSTSIGN": "{\"noncestr\":\"44729805311ed2cd0ac08f8b4cac5114\",\"timestamp\":1711421951,\"signature\":\"951d684dea7e703dc4970950fa15650f988c0eb3\"}",
            "xweb_xhr": "1"
        }
        self.url = 'https://captcha.fengkongcloud.com/ca/v1/register'

    def identify_gap(self, fg, bg):
        bg_img = cv2.imdecode(np.asarray(bytearray(bg), dtype=np.uint8), 0)  # 背景图片
        bg_img2 = bg_img.copy()  # 背景图片
        bg_pic2 = cv2.cvtColor(bg_img2, cv2.COLOR_GRAY2RGB)

        tp_img = cv2.imdecode(np.asarray(bytearray(fg), dtype=np.uint8), 0)  # 缺口图片
        # 识别图片边缘
        bg_img[bg_img < 60] = 0
        bg_img[bg_img >= 60] = 255
        bg_edge = cv2.Canny(bg_img, 0, 20)

        tp_edge = cv2.Canny(tp_img, 100, 200)
        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        # 缺口匹配
        s = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(s)  # 寻找最优匹配
        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        # cv2.rectangle(bg_pic2, tl, br, (0, 255, 255), 2)  # 绘制矩形
        # cv2.imwrite("3.png", bg_pic2)
        distance = tl[0]
        # 返回缺口的X坐标
        return distance

    def get_gap(self, bg, cut):
        return self.identify_gap(bg, cut)

    def getparms(self):
        params = {
            "organization": "eR46sBuqF0fdw7KWFLYa",
            "appId": "default",
            "channel": "miniProgram",
            "lang": "zh-cn",
            "model": "slide",
            "rversion": "1.0.1",
            "sdkver": "1.3.3",
            "data": "{}",
            "callback": "sm_" + timstr
        }
        response = requests.get(url=self.url, headers=self.headers, params=params)
        resp = re.findall(r'\(([^)]+)\)', response.text)[0]

        # resp = response.text.replace('sm_\d+(', '').replace(')', '')
        data = json.loads(resp)
        baseurl = 'https://castatic.fengkongcloud.cn'
        bg = baseurl + data['detail']['bg']
        fg = baseurl + data['detail']['fg']
        k = data['detail']['k']
        l = data['detail']['l']
        rid = data['detail']['rid']

        r = requests.get(url=bg, headers=self.headers).content
        r2 = requests.get(url=fg, headers=self.headers).content
        with open(r'bg.jpg', 'wb') as fp:
            fp.write(r)
        logger.info("背景图片下载完成")
        with open(r'fg.jpg', 'wb') as fp:
            fp.write(r2)
        logger.info("滑块图片下载完成")
        # logger.info(r,r2,k,l,rid)
        return r, r2, k, l, rid


if __name__ == '__main__':
    img = Img()
    img.getparms()

# headers = {
#     "Accept": "*/*",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Connection": "keep-alive",
#     "Content-Type": "application/json",
#     "Referer": "https://servicewechat.com/wxb296433268a1c654/108/page-frame.html",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "cross-site",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8447",
#     # "X-WECHAT-HOSTSIGN": "{\"noncestr\":\"44729805311ed2cd0ac08f8b4cac5114\",\"timestamp\":1711421951,\"signature\":\"951d684dea7e703dc4970950fa15650f988c0eb3\"}",
#     "xweb_xhr": "1"
# }
# url = "https://captcha.fengkongcloud.com/ca/v1/register"
# params = {
#     "organization": "eR46sBuqF0fdw7KWFLYa",
#     "appId": "default",
#     "channel": "miniProgram",
#     "lang": "zh-cn",
#     "model": "slide",
#     "rversion": "1.0.1",
#     "sdkver": "1.3.3",
#     "data": "{}",
#     "callback": "sm_"+timstr
# }
#
# def getparms():
#     response = requests.get(url, headers=headers, params=params)
#
#     resp = response.text.replace('sm_1711422319743(','').replace(')','')
#     data = json.loads(resp)
#     baseurl = 'https://castatic.fengkongcloud.cn'
#     bg = baseurl + data['detail']['bg']
#     fg = baseurl + data['detail']['fg']
#     k = data['detail']['k']
#     l = data['detail']['l']
#     rid = data['detail']['rid']
#
#     r =requests.get(url=bg,headers=headers).content
#     r2 =requests.get(url=fg,headers=headers).content
#     with open(r'bg.jpg','wb') as fp:
#         fp.write(r)
#     logger.info("背景图片下载完成")
#     with open(r'fg.jpg','wb') as fp:
#         fp.write(r2)
#     logger.info("滑块图片下载完成")
#     # logger.info(r,r2,k,l,rid)
#     return r,r2,k,l,rid
