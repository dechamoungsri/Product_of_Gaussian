
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # print Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/j/tscsdj01.dur')

    t = np.load('/work/w21/decha/Interspeech_2017/Result/02_no_consonant_weight_256/num_dct_cov_4/Beta_1.0/lf0/tscsdj01.npy')

    print np.nanmin(t)

    pass
