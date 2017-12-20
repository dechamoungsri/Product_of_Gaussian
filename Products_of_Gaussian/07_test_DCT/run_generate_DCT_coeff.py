
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

if __name__ == '__main__':

    syllable_dict_file = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary.pkl'

    d = Utility.load_obj(syllable_dict_file)

    coeff = 4

    syl_dct = dict()

    for name in d:

        data = d[name]
        w = PoGUtility.generate_W_for_DCT(len(data), coeff)

        data_dct = PoGUtility.generate_DCT(data, coeff) 
        data_dct = np.dot(w, data)

        i_dct = PoGUtility.generate_inverse_DCT(data_dct, 50)

        syl_dct[name] = data_dct

    print len(syl_dct)
    
    Utility.save_obj(syl_dct, '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_dct_given_mean_{}_coeff.pkl'.format(coeff))

    pass
