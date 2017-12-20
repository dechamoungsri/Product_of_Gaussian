
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


    org = '/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/tscsdj01.lf0'
    org = Utility.read_lf0_into_ascii(org)

    syn = '/work/w21/decha/Interspeech_2017/Result/From_03_with_mean_as_unvoice_lf0_format/num_dct_cov_7/tscsdj01.lf0'
    syn = np.loadtxt(syn)
    print syn[1000]

    syn = '/work/w21/decha/Interspeech_2017/Result/From_01_lf0_format/num_dct_cov_7/tscsdj01.lf0'
    syn = np.loadtxt(syn)
    print syn[1000]

    org[org==-1.00000000e+10] = np.nan
    syn[syn==-1.00000000e+10] = np.nan

    x = np.arange(len(org))

    print x.shape, org.shape

    plt.plot(x,org,label='org')
    plt.plot(x,syn,label='syn')

    plt.legend()
    plt.savefig('./test.eps')

    pass
