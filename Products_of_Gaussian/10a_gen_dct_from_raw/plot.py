
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

import sklearn, sklearn.metrics

if __name__ == '__main__':

    syllable_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary.pkl')
    coeff = 2
    name = 'tscsda04_31'

    data = syllable_dict[name]

    w = PoGUtility.generate_W_for_DCT(len(data), coeff)

    data_dct = PoGUtility.generate_DCT(data, coeff) 
    data_dct = np.dot(w, data)

    i_dct = PoGUtility.generate_inverse_DCT(data_dct, len(data))

    plt.plot( range( len(data) ), data, label='org')
    plt.plot( range( len(i_dct) ), i_dct, label='i_dct')

    plt.ylim([4.5, 6.0])

    plt.legend()
    plt.savefig('./{}_{}.eps'.format(name, coeff))

    pass
