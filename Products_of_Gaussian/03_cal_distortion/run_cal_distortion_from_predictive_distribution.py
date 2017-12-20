
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

if __name__ == '__main__':

    gpr = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/'

    org_path = '/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/'
    syn_path = '/work/w21/decha/Interspeech_2017/Result/From_03_with_mean_as_unvoice_lf0_format/num_dct_cov_7/'

    Distortion.lf0_distortion_syn_is_readable(org_path, syn_path)

    Distortion.lf0_distortion_syn_is_gpr_format(org_path, gpr)

    pass
