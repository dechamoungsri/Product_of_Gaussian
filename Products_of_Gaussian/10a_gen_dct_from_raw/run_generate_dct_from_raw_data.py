
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

from numpy.linalg import inv

import sklearn, sklearn.metrics

if __name__ == '__main__':

    syllable_dict_file = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary.pkl'

    all_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/syllable_database/02_add_stress_database_07_nov/dict_version.pkl')

    # print all_dict['tscsdh28_2']['dur']
    # print sum( all_dict['tscsdh28_2']['dur'][1:len(all_dict['tscsdh28_2']['dur'])])
    # sys.exit()

    d = Utility.load_obj(syllable_dict_file)

    coeff = 3

    syl_dct = dict()

    errors = dict()

    errors_list = []

    errors_tuple = []

    true = np.array([])
    dct_regen = np.array([])

    for name in d:

        data = d[name]
        w = PoGUtility.generate_W_for_DCT(len(data), coeff)

        data_dct = PoGUtility.generate_DCT(data, coeff) 
        data_dct = np.dot(w, data)

        i_dct = PoGUtility.generate_inverse_DCT(data_dct, len(data))

        true = np.concatenate((true, data))
        dct_regen = np.concatenate((dct_regen, i_dct))

        rmse = np.sqrt(sklearn.metrics.mean_squared_error(data, i_dct)) * 1200 / np.log(2)
        # print rmse
        errors[name] = rmse
        errors_list.append(rmse)

        if (int(all_dict[name]['stress']) == 1):
            syl_dct[name] = data_dct
        # else:
        #     print all_dict[name]['stress']

        dur = all_dict[name]['dur']
        vowel_dur = sum( all_dict[name]['dur'][1:len(all_dict[name]['dur'])]) / 50000

        errors_tuple.append( (name, rmse, vowel_dur) )

    # the histogram of the data
    n, bins, patches = plt.hist(errors_list, 100, normed=1, facecolor='green', alpha=0.75)

    plt.savefig('hist.eps')

    Utility.save_obj(errors, './errors_dict.pkl')

    rmse = np.sqrt(sklearn.metrics.mean_squared_error(true, dct_regen)) * 1200 / np.log(2)
    print 'all rmse : ', rmse

    Utility.sort_by_index(errors_tuple, 1)
    Utility.write_to_file_line_by_line('./errors_sorted.txt', errors_tuple)

    print len(syl_dct)
    
    # Utility.save_obj(syl_dct, '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_dct_3_stress_coeff.pkl'.format(coeff))

    pass
