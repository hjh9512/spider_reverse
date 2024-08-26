# -*- coding: utf-8 -*
'''
@Time     : 2023/07/28
@Author   : 14march
@Desc     :
'''
from io import BytesIO
import cv2
import numpy as np


def identify_gap(fg, bg):
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

def get_gap(bg, cut):
    return identify_gap(bg, cut)


if __name__ == '__main__':
    with open("./imgs/bg.jpg", "rb") as f:
        bg = f.read()
    with open("./imgs/fg.jpg", "rb") as f:
        cut = f.read()
    distance = get_gap(bg, cut)
    print(distance)