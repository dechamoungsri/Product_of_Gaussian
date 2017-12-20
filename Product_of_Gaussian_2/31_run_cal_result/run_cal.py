
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

def lf0_distortion_syn_is_gpr_format(org_path, syn_path):

    lf0_true_list = []
    lf0_pred_list = []

    for base in Utility.list_file(org_path) :
        
        if base.startswith('.'):
            continue

        b = Utility.get_basefilename(base)

        # Load Original
        original_file = os.path.join(org_path, base)
        original_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(original_file))
        
        # Load Synthesis
        synthesis_file = '{}/{}.npy'.format(syn_path, Utility.get_basefilename(base) )
        synthesis_vector = numpy.load(synthesis_file)
        synthesis_vector = synthesis_vector.reshape(len(synthesis_vector))

        synthesis_vector = np.nan_to_num(synthesis_vector)
        synthesis_vector[ np.where(synthesis_vector<=0.0) ] = UNDEF_VALUE

        for idx, (lf0_original, lf0_synthesis )in enumerate(zip(original_vector, synthesis_vector)):
            if lf0_original == UNDEF_VALUE:
                continue
            if lf0_synthesis == UNDEF_VALUE:
                continue

            lf0_true_list.append(lf0_original)
            lf0_pred_list.append(lf0_synthesis)

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
    print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

    pass

if __name__ == '__main__':

    UNDEF_VALUE = -1.00000000e+10

    org_for_distortion = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'
    # syn_for_distortion = '/work/w21/decha/Interspeech_2017/real_result/250_lf0/'

    # syn_for_distortion =  '/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/'

    syn_for_distortion =  '/work/w21/decha/Interspeech_2017/Result/250_training_of_frame-level/Syllable_training_size_950/all/Alpha_1.0_Beta_0.0/lf0/'

    lf0_distortion_syn_is_gpr_format(org_for_distortion, syn_for_distortion)

    pass
