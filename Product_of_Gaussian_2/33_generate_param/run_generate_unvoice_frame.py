
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

import getopt

import os
import sklearn, sklearn.metrics

import numpy

import array

if __name__ == '__main__':

    path = '/work/w21/decha/Interspeech_2017/real_result/single_450_lf0/'

    target_path = '/work/w21/decha/Interspeech_2017/real_result/single_250_lf0/'

    for i in range(1, 51):

        base = 'tscsdj{}'.format(Utility.fill_zero(i, 2))

        npy_path = '{}/{}.npy'.format(path, base )
        lf0 = np.load(npy_path)

        # print lf0
        unvoice = np.argwhere(np.isnan(lf0))

        target = np.load('{}/{}.npy'.format(target_path, base ))
        target[unvoice] = np.nan
        
        np.save('{}/{}.npy'.format(target_path, base ), target)

    pass
