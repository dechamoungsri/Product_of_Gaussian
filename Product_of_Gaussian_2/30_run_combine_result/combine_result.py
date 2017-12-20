
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

def gen_all_method(base):

    print base

    mono = '{}/{}.lab'.format(mono_label, base)
    stress_tone = '{}/{}.npy'.format(stress_list, base)

    lf0_out = np.array([])

    for line, (st, t) in zip( Utility.read_file_line_by_line(mono), np.load(stress_tone) ) :
        # print line, st, t

        l = Utility.trim(line)
        spl = l.split(' ')

        stress_type = 'unstress'
        if st == '1':
            stress_type = 'stress'

        if spl[2] in ['sil', 'pau']:
            target_file = original_file
        else:
            config = result_450['{}_{}'.format(stress_type, t)]

            if config['beta'] == '':
                target_file = original_file
            else:
                target_file = np.load( '{}/tone_{}/Alpha_1.0_Beta_{}_Gamma_{}/lf0/{}.npy'.format(config['basepath'], t, config['beta'], config['gamma'], base))

        start = int( float(spl[0]) / 50000.0)
        end = int( float(spl[1]) / 50000.0)

        # print target_file.shape

        target_lf0 = target_file[start:end]

        lf0_out = np.append(lf0_out, target_lf0, axis=0)

    print lf0_out.shape

    np.save('{}/{}.npy'.format(outpath, base), lf0_out)

    # sys.exit()

    pass

if __name__ == '__main__':

    print Utility.get_date_and_time_now()

    # outpath = '/work/w21/decha/Interspeech_2017/real_result/450_lf0/'
    # Utility.make_directory(outpath)

    # stress_list = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'
    # mono_label = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

    # stress_path = '/work/w21/decha/Interspeech_2017/Result/29_script/Exp_2_stress/Syllable_training_size_450/block_size_256/num_coeff_3/'
    # unstress_path = '/work/w21/decha/Interspeech_2017/Result/29_script/Exp_1_unstress/Syllable_training_size_450/block_size_256/num_coeff_3/'

    # single_path = '/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/'

    # result_450 = {
    #     'stress_0' : {
    #         'beta' : '2.2',
    #         'gamma' : '0.0',
    #         'basepath' : stress_path
    #     },
    #     'stress_1' : {
    #         'beta' : '',
    #         'gamma' : '',
    #         'basepath' : single_path
    #     },
    #     'stress_2' : {
    #         'beta' : '0.3',
    #         'gamma' : '0.0',
    #         'basepath' : stress_path
    #     },
    #     'stress_3' : {
    #         'beta' : '',
    #         'gamma' : '',
    #         'basepath' : single_path
    #     },
    #     'stress_4' : {
    #         'beta' : '2.2',
    #         'gamma' : '2.0',
    #         'basepath' : stress_path
    #     },


    #     'unstress_0' : {
    #         'beta' : '1.3',
    #         'gamma' : '1.5',
    #         'basepath' : unstress_path
    #     },
    #     'unstress_1' : {
    #         'beta' : '',
    #         'gamma' : '',
    #         'basepath' : single_path
    #     },
    #     'unstress_2' : {
    #         'beta' : '0.1',
    #         'gamma' : '0.5',
    #         'basepath' : unstress_path
    #     },
    #     'unstress_3' : {
    #         'beta' : '',
    #         'gamma' : '',
    #         'basepath' : single_path
    #     },
    #     'unstress_4' : {
    #         'beta' : '0.5',
    #         'gamma' : '0.5',
    #         'basepath' : unstress_path
    #     }
    # }

    outpath = '/work/w21/decha/Interspeech_2017/real_result/250_lf0/'
    Utility.make_directory(outpath)

    stress_list = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'
    mono_label = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

    stress_path = '/work/w21/decha/Interspeech_2017/Result/29_script/Exp_2_stress/Syllable_training_size_250/block_size_256/num_coeff_3/'
    unstress_path = '/work/w21/decha/Interspeech_2017/Result/29_script/Exp_1_unstress/Syllable_training_size_250/block_size_256/num_coeff_3/'

    single_path = '/work/w21/decha/Interspeech_2017/Result/05c_stress_only_iden_cov_block_256/num_dct_cov_3/Beta_0.0/lf0/'

    result_450 = {
        'stress_0' : {
            'beta' : '2.9',
            'gamma' : '0.0',
            'basepath' : stress_path
        },
        'stress_1' : {
            'beta' : '0.1',
            'gamma' : '0.0',
            'basepath' : stress_path
        },
        'stress_2' : {
            'beta' : '1.1',
            'gamma' : '0.0',
            'basepath' : stress_path
        },
        'stress_3' : {
            'beta' : '1.1',
            'gamma' : '0.1',
            'basepath' : stress_path
        },
        'stress_4' : {
            'beta' : '1.7',
            'gamma' : '0.9',
            'basepath' : stress_path
        },


        'unstress_0' : {
            'beta' : '1.7',
            'gamma' : '1.7',
            'basepath' : unstress_path
        },
        'unstress_1' : {
            'beta' : '',
            'gamma' : '',
            'basepath' : single_path
        },
        'unstress_2' : {
            'beta' : '0.3',
            'gamma' : '0.5',
            'basepath' : unstress_path
        },
        'unstress_3' : {
            'beta' : '',
            'gamma' : '',
            'basepath' : single_path
        },
        'unstress_4' : {
            'beta' : '1.1',
            'gamma' : '0.7',
            'basepath' : unstress_path
        }
    }

    for filename in Utility.list_file(mono_label):
        base = Utility.get_basefilename(filename)
        # print base

        original_file = np.load( '{}/{}.npy'.format(single_path, base) )

        gen_all_method(base)

    pass
