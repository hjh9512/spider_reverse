#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author     : 不愿
@Contact    : 1119035003@qq.com
@Software   : PyCharm
@File       : s1 
@ Time      : 2024-01-05 12:47
"""

import PIL
import cv2
import numpy as np
from PIL.ImagePath import Path
import json
import time
import execjs
import random
import requests


def __ease_out_expoone(sep):
    if sep == 1:
        return 1
    else:
        return 1 - pow(2, -10 * sep)


def get_slide_trackone(distance):
    if not isinstance(distance, int) or distance < 0:
        raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")
    slide_track = [
        [5, 1, int(time.time() * 1000), 0]
    ]
    # 共记录count次滑块位置信息
    count = 20 + int(distance / 3)
    # 初始化滑动时间
    t = random.randint(50, 100)
    # 记录上一次滑动的距离
    _x = 0
    _y = -12
    for i in range(count):
        # 已滑动的横向距离
        xx = __ease_out_expoone(i / count) * distance
        x = round(xx)
        # 滑动过程消耗的时间
        t = random.randint(10, 20)
        if x == _x:
            continue
        slide_track.append([x - _x, _y, t, 0])
        _x = x
    slide_track.append([1, 1, 12])
    n = 0
    for __ in slide_track[1:]:
        n += __[2]
    return slide_track, n


def imshow(img, winname='test', delay=0):
    """cv2展示图片"""
    cv2.imshow(winname, img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()


def pil_to_cv2(img):
    """
    pil转cv2图片
    :param img: pil图像, <type 'PIL.JpegImagePlugin.JpegImageFile'>
    :return: cv2图像, <type 'numpy.ndarray'>
    """
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


def bytes_to_cv2(img):
    """
    二进制图片转cv2
    :param img: 二进制图片数据, <type 'bytes'>
    :return: cv2图像, <type 'numpy.ndarray'>
    """
    # 将图片字节码bytes, 转换成一维的numpy数组到缓存中
    img_buffer_np = np.frombuffer(img, dtype=np.uint8)
    # 从指定的内存缓存中读取一维numpy数据, 并把数据转换(解码)成图像矩阵格式
    img_np = cv2.imdecode(img_buffer_np, 1)
    return img_np


def cv2_open(img, flag=None):
    """
    统一输出图片格式为cv2图像, <type 'numpy.ndarray'>
    :param img: <type 'bytes'/'numpy.ndarray'/'str'/'Path'/'PIL.JpegImagePlugin.JpegImageFile'>
    :param flag: 颜色空间转换类型, default: None
        eg: cv2.COLOR_BGR2GRAY（灰度图）
    :return: cv2图像, <numpy.ndarray>
    """
    if isinstance(img, bytes):
        img = bytes_to_cv2(img)
    elif isinstance(img, (str, Path)):
        img = cv2.imread(str(img))
    elif isinstance(img, np.ndarray):
        img = img
    elif isinstance(img, PIL.Image):
        img = pil_to_cv2(img)
    else:
        raise ValueError(f'输入的图片类型无法解析: {type(img)}')
    if flag is not None:
        img = cv2.cvtColor(img, flag)
    return img


def get_distance(bg, tp, im_show=False, save_path=None):
    """
    :param bg: 背景图路径或Path对象或图片二进制
        eg: 'assets/bg.jpg'
            Path('assets/bg.jpg')
    :param tp: 缺口图路径或Path对象或图片二进制
        eg: 'assets/tp.jpg'
            Path('assets/tp.jpg')
    :param im_show: 是否显示结果, <type 'bool'>; default: False
    :param save_path: 保存路径, <type 'str'/'Path'>; default: None
    :return: 缺口位置
    """
    # 读取图片
    bg_img = cv2_open(bg)
    tp_gray = cv2_open(tp, flag=cv2.COLOR_BGR2GRAY)[490:610, 140:260]

    # 金字塔均值漂移
    bg_shift = cv2.pyrMeanShiftFiltering(bg_img, 5, 50)

    # 边缘检测
    tp_gray = cv2.Canny(tp_gray, 255, 255)
    bg_gray = cv2.Canny(bg_shift, 255, 255)

    # 目标匹配
    result = cv2.matchTemplate(bg_gray, tp_gray, cv2.TM_CCOEFF_NORMED)
    # 解析匹配结果
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # distance = max_loc[0]
    # if save_path or im_show:
    #     # 需要绘制的方框高度和宽度
    #     tp_height, tp_width = tp_gray.shape[:2]
    #     # 矩形左上角点位置
    #     x, y = max_loc
    #     # 矩形右下角点位置
    #     _x, _y = x + tp_width, y + tp_height
    #     # 绘制矩形
    #     bg_img = cv2_open(bg)
    #     cv2.rectangle(bg_img, (x, y), (_x, _y), (0, 0, 255), 2)
    #     # 保存缺口识别结果到背景图
    #     if save_path:
    #         save_path = Path(save_path).resolve()
    #         save_path = save_path.parent / f"{save_path.stem}.{distance}{save_path.suffix}"
    #         save_path = save_path.__str__()
    #         cv2.imwrite(save_path, bg_img)
    #     # 显示缺口识别结果
    #     if im_show:
    #         imshow(bg_img)
    print(max_loc)
    # return distance
    return max_loc


def prehandle():
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.urbtix.hk/login?redirect=%2Fshopping-cart",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://turing.captcha.qcloud.com/cap_union_prehandle"
    params = {
        "aid": "195126592",
        "protocol": "https",
        "accver": "1",
        "showtype": "popup",
        "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExOS4wLjYwNDUuMTYwIFNhZmFyaS81MzcuMzY=",
        "noheader": "1",
        "fb": "1",
        "aged": "0",
        "enableAged": "0",
        "enableDarkMode": "0",
        "grayscale": "1",
        "clientype": "2",
        "lang": "zh-cn",
        "userLanguage": "zh-cn",
        "cap_cd": "",
        "uid": "",
        "entry_url": "https://www.urbtix.hk/login",
        "elder_captcha": "0",
        "js": "/tcaptcha-frame.22125576.js",
        "login_appid": "",
        "wb": "2",
        "subsid": "11",
        "callback": "_aq_946707",
        "sess": ""
    }
    response = requests.get(url, headers=headers, params=params)
    response = json.loads(response.text[11:-1])
    img_url = response['data']['dyn_show_info']['bg_elem_cfg']['img_url']
    sprite_url = response['data']['dyn_show_info']['sprite_url']
    pow_answer = response['data']['comm_captcha_cfg']['pow_cfg']['prefix']
    nonce = response['data']['comm_captcha_cfg']['pow_cfg']['md5']
    # tdc_path = response['data']['comm_captcha_cfg']['tdc_path']
    sess = response['sess']
    bg = requests.get('https://turing.captcha.qcloud.com' + img_url).content
    tp = requests.get('https://turing.captcha.qcloud.com' + sprite_url).content
    with open('cap_union_new_getcapbysig.png', 'wb') as f:
        f.write(bg)

    with open('tp.png', 'wb') as f:
        f.write(tp)

    return sess, pow_answer, nonce


def get_data():
    sess, pow_answer, nonce = prehandle()

    with open('cap_union_new_getcapbysig.png', 'rb') as f:
        bg = f.read()

    with open('tp.png', 'rb') as f:
        tp = f.read()

    with open('ans.js', 'r') as f:
        cc1 = f.read()

    with open('tx_tea.js', 'r', encoding="utf-8") as f:
        dd = f.read()

    tl = get_distance(bg, tp, im_show=False, save_path=None)

    ctx = execjs.compile(dd)
    ctx1 = execjs.compile(cc1)
    trackone, tim = get_slide_trackone(tl[0] - 2)

    collect = ctx.call('coollect', trackone)
    ts = random.randint(80, 200)

    ts_1 = ctx1.call('getWorkloadResult', {"target": nonce, "nonce": pow_answer})
    # print(ts_1)
    data = {
        'collect': collect,
        'tlg': len(collect),
        'eks': "WgZobKET/nkgdY49gsNZjDqLn1vi3eidquuJPG6ekkyyYqXTDuzyquoNu6a0cRvOukg/57Sjz6otaYrgNGIsX6Bfpd9HMNHJazWQShA5PRcbv26zRWEpBiPOfDBlF4KmcYgywSoT5+wWxqyW0tesiYJ7sTSl4efLo0LRB4/vnvhqMFVtmK4b7KoKfjqEkzWMGkgHObDtolD2ckdGI6I/xYaMsM52jbuGnUlAWAtQ9v8=",
        'sess': sess,
        'ans': json.dumps([{"elem_id": 1, "type": "DynAnswerType_POS", "data": f"{tl[0] - 2},{tl[1]}"}]),
        'pow_answer': f"{pow_answer}{ts_1['ans']}",
        'pow_calc_time': ts_1['duration']
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://turing.captcha.gtimg.com",
        "Pragma": "no-cache",
        "Referer": "https://turing.captcha.gtimg.com/1/template/drag_ele.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://turing.captcha.qcloud.com/cap_union_new_verify"

    # time.sleep(1)
    response = requests.post(url, headers=headers, data=data)
    print(response.text)


if __name__ == '__main__':
    tim = time.time()
    for i in range(10):
        get_data()
    print(time.time() - tim)
    # print(get_slide_trackone(60))
