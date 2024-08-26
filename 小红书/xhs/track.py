# -*- coding: utf-8 -*
'''
@Time     : 2023/02/15
@Author   : scout
@Desc     :
'''
import random
import time


class Track(object):
    '''
    滑动轨迹的生成
    '''
    p = [[0, 0, 0], [0, 0, 111], [0, 0, 203], [33, 0, 301], [44, 0, 401], [72, 0, 501], [91, 0, 601], [100, 0, 702],
         [118, 0, 801], [136, 0, 901], [155, 0, 1001], [159, 0, 1102], [168, 0, 1200], [168, 0, 1303], [168, 0, 1401],
         [171, 0, 1511], [172, 0, 1600], [172, 0, 1704], [172, 0, 1810], [172, 0, 1901], [174, 0, 2014], [176, 0, 2103],
         [176, 0, 2202], [176, 0, 2308], [176, 0, 2401], [176, 0, 2516], [176, 0, 2613], [176, 0, 2707], [176, 0, 2814],
         [177, 0, 2901], [177, 0, 3006], [177, 0, 3102], [177, 0, 3216], [177, 0, 3310], [177, 0, 3401], [177, 0, 3512],
         [178, 0, 3601], [178, 0, 3702], [178, 0, 3812], [178, 0, 3901], [178, 0, 4001], [178, 0, 4110], [178, 0, 4203]]

    @classmethod
    def get_slice_track(cls, target_point):
        scale_factor = target_point / cls.p[-1][0]
        new_path = [cls.generate_path(x, scale_factor) for x in cls.p]
        return new_path

    @staticmethod
    def generate_path(pointer, scale_factor):
        x = pointer[0]
        y = pointer[1]
        t = pointer[2]
        return [int(x * scale_factor), y, t]


if __name__ == '__main__':
    print(Track.get_slice_track(50))