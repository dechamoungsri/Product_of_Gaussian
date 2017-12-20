
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

    unvoice = -1.00000000e+10

    syllable_dct_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_dct_given_mean.pkl')

    training_set = [
        'a', 'b', 'c', 'd', 'e', 
        'f', 'g', 'h', 'i' ]

    o = []

    for n in syllable_dct_dict:
        if n[5] in training_set:
            # print n
            o.append(syllable_dct_dict[n])

    o = np.array(o)
    var = np.var(o, axis=0)

    print var

    Utility.save_obj(var, '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_dct_a-i_variance.pkl')

    pass
