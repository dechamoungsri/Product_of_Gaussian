
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

    # syn = np.load('/work/w21/decha/Interspeech_2017/Result/01_Given_syllable_dct_Joint_probability/num_dct_cov_7/tscsdj01.npy')

    method = '01_Given_syllable_model_combined_128'
    filename = 'tscsdj01'

    syn = np.load('/work/w21/decha/Interspeech_2017/Result/{}/num_dct_cov_7/{}.npy'.format(method, filename))

    speech_param = np.load('/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05a_GPR/testrun/out/tsc/a-i/speech_param/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/param_mean/{}.npy'.format(filename))

    org = Utility.read_lf0_into_ascii('/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/{}.lf0'.format(filename))

    org = np.array(org)

    idx = np.where(speech_param==unvoice)[0]

    syn[idx] = np.nan
    speech_param[idx] = np.nan
    org[np.where(org==unvoice)[0]] = np.nan

    x = range(len(syn))

    fig = plt.gcf()
    fig.set_size_inches(15, 4)
    plt.plot(x , syn, label='Decha syn')
    plt.plot(x , speech_param, label='Koriyama syn')
    plt.plot(x , org, label='Original')
    # plt.ylim([10, 0])
    # plt.xlim([600,1000])
    plt.legend()
    plt.savefig('./{}_{}.eps'.format(method, filename))

    pass
