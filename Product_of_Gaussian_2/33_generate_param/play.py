
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

import getopt

import os
import sklearn, sklearn.metrics

import numpy

import array

if __name__ == '__main__':

    # bap = np.load('/work/w22/decha/decha_w22/speccom1/Speech_synthesis_w22/GPR_for_generate_speech/testrun/out/tsc/a-t/speech_param/a-t/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/param_mean/tscsdj01.npy')

    mcep = np.load('/work/w22/decha/decha_w22/speccom1/Speech_synthesis_w22/GPR_for_generate_speech/testrun/out/tsc/a-t/speech_param_syn/a-t/demo/seed-00/M-1024/B-1024/num_iters-5/mcep/param_mean/tscsdj01.npy')
    print mcep.shape

    bap = np.load('/work/w22/decha/decha_w22/speccom1/Speech_synthesis_w22/GPR_for_generate_speech/testrun/out/tsc/a-t/speech_param/a-t/demo/seed-00/M-1024/B-1024/num_iters-5/bap/param_mean/tscsdj37.npy')
    print bap.shape

    lf0 = np.load('/work/w22/decha/decha_w22/speccom1/Speech_synthesis_w22/GPR_for_generate_speech/testrun/out/tsc/a-t/speech_param_syn/a-t/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/param_mean/tscsdj01.npy')
    lf0 = np.load('/work/w21/decha/Interspeech_2017/real_result/single_450_lf0/tscsdj01.npy')
    print lf0
    print lf0.shape, len(lf0[lf0<0])

    # dur = np.load('/work/w22/decha/decha_w22/speccom1/Speech_synthesis_w22/GPR_for_generate_speech/testrun/out/tsc/a-t/speech_param/a-t/demo/seed-00/M-1024/B-1024/num_iters-5/predicted_dur/param_mean/tscsdj01.npy')
    # print dur

    pass
