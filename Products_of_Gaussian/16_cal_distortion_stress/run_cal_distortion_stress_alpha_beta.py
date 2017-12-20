
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

def lf0_distortion_syn_is_gpr_format(org_path,syn_path, stress_list, mono_label):
    
    lf0_true_list = []
    lf0_pred_list = []
    
    lf0_true_stress_list = []
    lf0_pred_stress_list = []

    for base in Utility.list_file(org_path) :
        
        if base.startswith('.'):
            continue

        b = Utility.get_basefilename(base)
        stress = np.load('{}/{}.npy'.format(stress_list, b))
        mono_file = Utility.read_file_line_by_line('{}/{}.lab'.format(mono_label, b))

        stress_index = np.array([])

        for st, mono in zip(stress, mono_file):
            spl = mono.split(' ')
            start = int(spl[0])/50000
            end = int(spl[1])/50000

            if st == '1':
                stress_index = np.append(stress_index, np.arange(start, end), axis=0 )

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

        for idx, (lf0_original, lf0_synthesis )in enumerate(zip(original_vector, synthesis_vector)):
            if lf0_original == UNDEF_VALUE:
                continue
            if lf0_synthesis == UNDEF_VALUE:
                continue

            lf0_true_list.append(lf0_original)
            lf0_pred_list.append(lf0_synthesis)

            if idx in stress_index:
                lf0_true_stress_list.append(lf0_original)
                lf0_pred_stress_list.append(lf0_synthesis)

    # rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1000 / numpy.log(2)
    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
    print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_stress_list, lf0_pred_stress_list)) * 1200 / numpy.log(2)
    print('Only stress LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_stress_list)))

    pass

if __name__ == '__main__':

    UNDEF_VALUE = -1.0e+10

    stress_list = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'
    mono_label = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

    org = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'

    syn = '/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/'

    lf0_distortion_syn_is_gpr_format(org, syn, stress_list, mono_label)

    for a in np.arange(0.1, 2.1, 0.2):
        for i in np.arange(0.1, 2.1, 0.2):

            print 'Alpha: ', a , 'Beta : ', i
            a = 1.0
            i = 1.5

            syn = '/work/w21/decha/Interspeech_2017/Result/05f_stress_only_iden_cov_remove_head_tail_original_vuv_block_256/num_dct_cov_3/Alpha_{}_Beta_{}/lf0/'.format(a, i)

            # syn = '/work/w21/decha/Interspeech_2017/Result/05d_stress_only_real_cov_block_256/num_dct_cov_3/Beta_{}/lf0/'.format(i)

            lf0_distortion_syn_is_gpr_format(org, syn, stress_list, mono_label)

            sys.exit()

    pass
