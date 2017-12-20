
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

import os
import sklearn, sklearn.metrics

def lf0_distortion_syn_is_gpr_format(org_path, data_dict, stress_list, mono_label, tone, stress_type):
    
    UNDEF_VALUE = -1.0e+10

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

        # Load Synthesis
        synthesis_vector = data_dict['initial'][1][b]

        for st, mono in zip(stress, mono_file):
            spl = mono.split(' ')
            start = int(spl[0])/50000
            end = int(spl[1])/50000

            if not (st[0] == '1'):
                st[0] = '0'

            if (st[0] == str(stress_type)) :

                if str(st[2]) == '0':
                    pt = 'initial'
                elif str(st[2]) == '1':
                    pt = 'vowel'
                elif str(st[2]) == '2':
                    pt = 'final'

                synthesis_vector[start: end] = data_dict[pt][int(st[1])][b][start: end]

                if '{}'.format(tone) == 'all':
                    stress_index = np.append(stress_index, np.arange(start, end), axis=0 )
                elif st[1] == '{}'.format(tone) :
                    stress_index = np.append(stress_index, np.arange(start, end), axis=0 )

        # Load Original
        original_file = os.path.join(org_path, base)
        original_vector = np.loadtxt(Utility.read_lf0_into_ascii(original_file))

        # print synthesis_vector
        synthesis_vector = np.nan_to_num(synthesis_vector)
        synthesis_vector[ np.where(synthesis_vector<=0.0) ] = UNDEF_VALUE

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

    print 'Stress {}, Tone {}'.format(stress_type, tone)

    rmse = np.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / np.log(2)
    print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

    rmse = np.sqrt(sklearn.metrics.mean_squared_error(lf0_true_stress_list, lf0_pred_stress_list)) * 1200 / np.log(2)
    print('Only specific case LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_stress_list)))

    return rmse

    pass


if __name__ == '__main__':

    data_dict = dict()

    for phone in ['initial', 'vowel', 'final']:
        data_dict[phone] = dict()
        for tone in [0, 1, 2, 3, 4]:
            data_dict[phone][tone] = Utility.load_obj('/work/w21/decha/Interspeech_2017/Result_4/Stress_Method_C_phone_syllable_tone_separated_{}_2017-05-24/Syllable_training_size_250_block_size_256_num_coeff_3/tone_{}/lf0_generated.pkl'.format(phone, tone))

    # print data_dict

    org_for_distortion = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'

    stress_list = '/work/w2/decha/Data/GPR_speccom_data/01_phone_level_data/stress_list/j/'
    mono_label = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/j/'

    stress_type = '1'

    for tone in ['all', 0, 1, 2, 3, 4]:
        lf0_distortion_syn_is_gpr_format(org_for_distortion, data_dict, stress_list, mono_label, tone, stress_type)

    pass
