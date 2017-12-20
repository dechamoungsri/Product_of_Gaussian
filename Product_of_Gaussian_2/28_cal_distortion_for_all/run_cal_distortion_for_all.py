
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

def lf0_distortion_syn_is_gpr_format(org_path,syn_path, stress_list, mono_label, stress_type):

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

            if stress_type == 1:
                if (st[0] == '1') & ( st[1] == '{}'.format(tone) ):
                    stress_index = np.append(stress_index, np.arange(start, end), axis=0 )
            else:
                if (st[0] != '1') & ( st[1] == '{}'.format(tone) ):
                    stress_index = np.append(stress_index, np.arange(start, end), axis=0 )

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

            if idx in stress_index:
                lf0_true_stress_list.append(lf0_original)
                lf0_pred_stress_list.append(lf0_synthesis)

    # rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
    # print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

    # rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_stress_list, lf0_pred_stress_list)) * 1200 / numpy.log(2)
    # print('Only stress LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_stress_list)))

    # rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_tone_list, lf0_pred_tone_list)) * 1200 / numpy.log(2)
    # print('Tone {} LF0 RMSE: {:f} in {} frames'.format( tone, rmse, len(lf0_true_tone_list)))

    pass

if __name__ == '__main__':

    unvoice_value = -1.00000000e+10
    UNDEF_VALUE = unvoice_value

    stress_list = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'
    mono_label = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

    org_for_distortion = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'

    synthesis_250_list = [
        ('/work/w21/decha/Interspeech_2017/Result/C2-250-frame-utterance/Syllable_training_size_250/block_size_256/num_coeff_3/tone_0/Alpha_1.0_Beta_2.9/lf0/', 0, 1),
        ('/work/w21/decha/Interspeech_2017/Result/C2-250-frame-utterance/Syllable_training_size_250/block_size_256/num_coeff_3/tone_1/Alpha_1.0_Beta_0.1/lf0/', 1, 1),
        ('/work/w21/decha/Interspeech_2017/Result/C2-250-frame-utterance/Syllable_training_size_250/block_size_256/num_coeff_3/tone_2/Alpha_1.0_Beta_1.1/lf0/', 2, 1),
        ('/work/w21/decha/Interspeech_2017/Result/C2-250-frame-utterance/Syllable_training_size_250/block_size_256/num_coeff_3/tone_3/Alpha_1.0_Beta_0.9/lf0/', 3, 1),
        ('/work/w21/decha/Interspeech_2017/Result/C5_two_optimal_value/Syllable_training_size_250/block_size_256/num_coeff_3/tone_4/Alpha_1.0_Beta_1.1_Gamma_1.9/lf0/', 4, 1),

        ('/work/w21/decha/Interspeech_2017/Result/Script_26/Exp_1_no_zeroth_fix/Syllable_training_size_250/block_size_256/num_coeff_3/tone_0/Alpha_1.0_Beta_1.7/lf0/', 0, 0),
        ('/work/w21/decha/Interspeech_2017/Result/250_training_of_frame-level/Syllable_training_size_950/all/Alpha_1.0_Beta_0.0/lf0/', 1, 0),
        ('/work/w21/decha/Interspeech_2017/Result/Script_26/Exp_1_no_zeroth_fix/Syllable_training_size_250/block_size_256/num_coeff_3/tone_2/Alpha_1.0_Beta_0.3/lf0/', 2, 0),
        ('/work/w21/decha/Interspeech_2017/Result/250_training_of_frame-level/Syllable_training_size_950/all/Alpha_1.0_Beta_0.0/lf0/', 3, 0),
        ('/work/w21/decha/Interspeech_2017/Result/Script_26/Exp_1_no_zeroth_fix/Syllable_training_size_250/block_size_256/num_coeff_3/tone_4/Alpha_1.0_Beta_1.1/lf0/', 4, 0),
    ]

    synthesis_450_list = [
        ('/work/w21/decha/Interspeech_2017/Result/B_Remove_zeroth_from_all/Syllable_training_size_950/block_size_256/num_coeff_3/tone_0/Alpha_1.0_Beta_1.7/lf0/', 0, 1),
        ('/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/', 1, 1),
        ('/work/w21/decha/Interspeech_2017/Result/B_Remove_zeroth_from_all/Syllable_training_size_950/block_size_256/num_coeff_3/tone_2/Alpha_1.0_Beta_0.3/lf0/', 2, 1),
        ('/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/', 3, 1),
        ('/work/w21/decha/Interspeech_2017/Result/B_Remove_zeroth_from_all/Syllable_training_size_950/block_size_256/num_coeff_3/tone_4/Alpha_1.0_Beta_1.5/lf0/', 4, 1),

        ('/work/w21/decha/Interspeech_2017/Result/Script_26/Exp_1_no_zeroth_fix/Syllable_training_size_450/block_size_256/num_coeff_3/tone_0/Alpha_1.0_Beta_1.3/lf0/', 0, 0),
        ('/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/', 1, 0),
        ('/work/w21/decha/Interspeech_2017/Result/C5_two_optimal_value/Syllable_training_size_450/block_size_256/num_coeff_3/tone_2/Alpha_1.0_Beta_0.1_Gamma_0.5/lf0/', 2, 0),
        ('/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/', 3, 0),
        ('/work/w21/decha/Interspeech_2017/Result/Script_26/Exp_1_no_zeroth_fix/Syllable_training_size_450/block_size_256/num_coeff_3/tone_4/Alpha_1.0_Beta_0.5/lf0/', 4, 0),
    ]

    lf0_true_stress_list = []
    lf0_pred_stress_list = []

    for tup in synthesis_250_list:

        syn_path = tup[0]
        tone = tup[1]
        stress_type = tup[2]

        lf0_distortion_syn_is_gpr_format(org_for_distortion,syn_path, stress_list, mono_label, stress_type)

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_stress_list, lf0_pred_stress_list)) * 1200 / numpy.log(2)
    print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_stress_list)))

    pass
