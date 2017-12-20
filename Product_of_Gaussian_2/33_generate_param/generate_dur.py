
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

    mono_path = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/'
    mono_for_gpr_path = '/work/w2/decha/Data/GPR_speccom_data/mono_for_gpr_gen/tsc/sd/'

    for sett in Utility.char_range('a', 'z'):

        Utility.make_directory('{}/{}/'.format(mono_for_gpr_path, sett))

        for i in range(1, 51):

            base = 'tscsd{}{}'.format(sett, Utility.fill_zero(i, 2) )

            mono = '{}/{}/{}.lab'.format(mono_path, sett, base)
            mono_for_gpr = '{}/{}/{}.npy'.format(mono_for_gpr_path, sett, base)

            out = []

            for line in Utility.read_file_line_by_line(mono):
                l = Utility.trim(line).split(' ')
                out.append( [ (float(l[1]) - float(l[0]))/10000000 ] )

            print out
            np.save(mono_for_gpr, np.array(out))

    pass
