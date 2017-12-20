
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

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

if __name__ == '__main__':

    label_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/syllable_time/'

    start = sys.argv[1]
    end = sys.argv[2]

    all_dur = 0

    for i in Utility.char_range(start, end):
        set_path = '{}/{}/'.format(label_path, i)

        for n in range(1, 51):
            filepath = '{}/tscsd{}{}.lab'.format(set_path, i, Utility.fill_zero(n, 2))

            for line in Utility.read_file_line_by_line(filepath):
                l = Utility.trim(line)
                spl = l.split(' ')
                if spl[2] in ['sil-sil+sil-x', 'pau-pau+pau-x']:
                    print spl[2]
                    continue
                else:
                    all_dur = all_dur + (int(spl[1]) - int(spl[0]))

    print all_dur
    print float(all_dur)/10000000.0 / 60.0

    pass
