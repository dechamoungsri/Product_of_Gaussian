
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
import numpy

import sklearn, sklearn.metrics

def lf0_distortion_syn_is_gpr_format(org_path,syn_path):
    
    lf0_true_list = []
    lf0_pred_list = []
    
    for base in Utility.list_file(org_path) :
        
        if base.startswith('.'):
            continue
        
        # if '12' in base: continue

        # Load Original
        original_file = os.path.join(org_path, base)
        original_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(original_file))
        
        # Load Synthesis
        synthesis_file = '{}/{}.npy'.format(syn_path, Utility.get_basefilename(base) )
        synthesis_vector = numpy.load(synthesis_file)
        synthesis_vector = synthesis_vector.reshape(len(synthesis_vector))

        # print synthesis_vector
# 
        synthesis_vector = np.nan_to_num(synthesis_vector)
        synthesis_vector[ np.where(synthesis_vector<=0.0) ] = UNDEF_VALUE

        # print synthesis_vector

        # sys.exit()

        for lf0_original, lf0_synthesis in zip(original_vector, synthesis_vector):
            if lf0_original == UNDEF_VALUE:
                continue
            if lf0_synthesis == UNDEF_VALUE:
                continue

            lf0_true_list.append(lf0_original)
            lf0_pred_list.append(lf0_synthesis)

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
    print('LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

    pass

if __name__ == '__main__':

    UNDEF_VALUE = -1.0e+10

    org = '/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/'

    syn = '/work/w21/decha/Interspeech_2017/Result/01_combined_weight_256/num_dct_cov_4/Beta_0.0/lf0/'

    lf0_distortion_syn_is_gpr_format(org, syn)

    alpha = 0.2001

    for i in np.arange(0.1, 2.1, 0.1):
    # for i in np.arange(0.01, 1.0, 0.01):

        print 'Beta : ', i

        syn = '/work/w21/decha/Interspeech_2017/Result/04-950-b_stress_only_original_vuv_block_256/num_dct_cov_3/Alpha_{}_Beta_{}/lf0/'.format(alpha, i)

        lf0_distortion_syn_is_gpr_format(org, syn)

    pass
