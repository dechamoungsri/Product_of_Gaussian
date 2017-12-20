
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

def gen_dct(syllable_dict):

    syl_dict = Utility.load_obj(syllable_dict)

    for syl in syl_dict:

        data = syl_dict[syl]
        syl_dct_dict[syl] = np.column_stack(
                (
                    dct(data[0], norm='ortho'), 
                    dct(data[1], norm='ortho'), 
                    dct(data[2], norm='ortho')
                )
            )

        print syl_dct_dict[syl]
        print syl_dct_dict[syl].shape


    pass

if __name__ == '__main__':

    syllable_dict_file = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_data_with_delta_deltadelta.pkl'

    syl_dct_dict = dict()

    gen_dct(syllable_dict_file)

    Utility.save_obj(syl_dct_dict, '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dct_with_delta_dictionary.pkl')

    pass
