
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

        # print syl

        lf0 = syl_dict[syl]
        lf0_dct = dct(lf0, norm='ortho')
        lf0_idct = idct(lf0_dct, norm='ortho')

        syl_dct_dict[syl] = lf0_dct


    pass

if __name__ == '__main__':

    syllable_dict_file = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary.pkl'

    syl_dct_dict = dict()

    gen_dct(syllable_dict_file)

    Utility.save_obj(syl_dct_dict, '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dct_dictionary.pkl')

    pass
