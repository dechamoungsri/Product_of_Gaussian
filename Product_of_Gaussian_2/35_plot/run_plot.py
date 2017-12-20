
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


def lf0_distortion_syn_is_gpr_format(original_vector, synthesis_vector):

    lf0_true_list = []
    lf0_pred_list = []

    for idx, (lf0_original, lf0_synthesis )in enumerate(zip(original_vector, synthesis_vector)):
        if lf0_original == UNDEF_VALUE:
            continue
        if lf0_synthesis == UNDEF_VALUE:
            continue

        lf0_true_list.append(lf0_original)
        lf0_pred_list.append(lf0_synthesis)

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
    # print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))
    return rmse

    pass

if __name__ == '__main__':

    UNDEF_VALUE = -1.00000000e+10

    original = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'

    out_path = '/work/w21/decha/Interspeech_2017/plot/single-multi-450/'
    Utility.make_directory(out_path)
    paths = [
        # ['/work/w21/decha/Interspeech_2017/real_result/single_250_lf0/', '/work/w21/decha/Interspeech_2017/real_result/multi_250_lf0/'],
        ['/work/w21/decha/Interspeech_2017/real_result/single_450_lf0/', '/work/w21/decha/Interspeech_2017/real_result/multi_450_lf0/']
        # ['/work/w21/decha/Interspeech_2017/real_result/single_250_lf0/', '/work/w21/decha/Interspeech_2017/real_result/single_450_lf0/']
    ]

    for path in paths:

        for i in range(1, 51):

            base = 'tscsdj{}'.format(Utility.fill_zero(i, 2))

            lf0_single = np.load('{}/{}.npy'.format(path[0], base))
            lf0_multi = np.load('{}/{}.npy'.format(path[1], base))

            print base
            single_vs_multi_rmse = lf0_distortion_syn_is_gpr_format(lf0_single, lf0_multi)

            original_lf0 = Utility.read_lf0_into_ascii('{}/{}.lf0'.format(original, base))

            single = lf0_distortion_syn_is_gpr_format(lf0_single, original_lf0)
            multi = lf0_distortion_syn_is_gpr_format(lf0_multi, original_lf0)

            print single_vs_multi_rmse, single, multi, 'Improve : ', (single-multi)

            plt.clf()

            fig = plt.gcf()
            fig.set_size_inches(15, 4)

            original_lf0[original_lf0<0] = np.nan
            lf0_single[lf0_single<0] = np.nan
            lf0_multi[lf0_multi<0] = np.nan

            x = range(len(original_lf0))
            plt.plot(x, original_lf0, 'k--', alpha=0.5, label='original')
            plt.plot(range(len(lf0_single)), lf0_single, 'r', alpha=0.5, label='single')
            plt.plot(range(len(lf0_multi)), lf0_multi, 'blue', alpha=0.5, label='multi')
            plt.legend()
            plt.savefig('{}/{}.pdf'.format(out_path, base))

            # sys.exit()

    pass
