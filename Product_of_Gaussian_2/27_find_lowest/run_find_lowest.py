
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../../Products_of_Gaussian/')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility
from PoG_Utility.plot_utility import PlotUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct
from numpy.linalg import inv

from sklearn.metrics.pairwise import rbf_kernel

from scipy import array, linalg, dot

import os
import sklearn, sklearn.metrics

import numpy
import argparse

from time import gmtime, strftime


if __name__ == '__main__':

    run_all_coeff_unstress = [
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/run_all_coefficient_unstress/log_Exp_3/log.0.250.02:25:24.755232.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/run_all_coefficient_unstress/log_Exp_3/log.1.250.07:37:00.839330.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/run_all_coefficient_unstress/log_Exp_3/log.2.250.13:48:48.259375.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/run_all_coefficient_unstress/log_Exp_3/log.3.250.14:51:18.836113.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/run_all_coefficient_unstress/log_Exp_3/log.4.250.15:53:39.586523.txt'
    ]

    tars = ['/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/stress/log_Exp_2/log.4.450.21:49:04.369134.txt']

    stress_450_three_optimization = [
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/stress/log_Exp_2/log.0.450.23:23:28.235108.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/stress/log_Exp_2/log.1.450.00:00:14.972609.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/stress/log_Exp_2/log.2.450.00:38:23.486544.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/stress/log_Exp_2/log.3.450.01:15:50.907911.txt',
        '/work/w21/decha/Interspeech_2017/Product_of_Gaussian_2/29_run_keep_result/stress/log_Exp_2/log.4.450.02:10:26.865873.txt'
    ]

    for target_file in tars:

        opt = ''
        rmse = 10000000.0

        cur_val = ''

        for line in Utility.read_file_line_by_line(target_file):
            if 'Beta' in line:
                cur_val = Utility.trim(line)

            if 'Only' in line:
                r = line.split(' ')[4]
                # print r
                if float(r) < float(rmse):
                    # print rmse, r
                    rmse = r
                    opt = cur_val

        print opt
        print rmse

    pass
