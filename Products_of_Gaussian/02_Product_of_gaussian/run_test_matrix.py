
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

import math

if __name__ == '__main__':

    syllable_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_data_with_delta_deltadelta.pkl')

    for syl in syllable_dict:

        print syl

        lf0 = syllable_dict[syl][0]

        y = 0.0
        for n, f in enumerate(lf0):
            y = y + f * math.cos(math.pi*0*(2.0*n+1)/(2.0* len(lf0) ) )


        W = PoGUtility.generate_W_for_DCT(len(lf0), len(lf0))


        lf0_dct = dct(lf0, norm='ortho')

        print lf0_dct

        sys.exit()

    pass
