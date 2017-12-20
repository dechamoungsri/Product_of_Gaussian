
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

    syllable_dict_file = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary.pkl'

    d = Utility.load_obj(syllable_dict_file)

    name = 'tscsda01_19'

    data = d[name]
    # print data

    x = xrange(len(data))
    plt.plot(x, data, 'k--', label='org')

    # for c in range(1, 20, 2):
    for c in [1,2,3,4,5,6,7]:

        coeff = c

        w = PoGUtility.generate_W_for_DCT(len(data), coeff)

        data_dct = PoGUtility.generate_DCT(data, coeff) 
        data_dct = np.dot(w, data)

        # print 'data dct', data_dct

        i_dct = PoGUtility.generate_inverse_DCT(data_dct, 50)

        print data_dct.shape

        # plt.clf()
        
        plt.plot( np.linspace(0, len(x), len(i_dct)) , i_dct, label='i_dct_{}'.format(c))

    plt.legend()
    plt.savefig('{}_coeff.eps'.format(name))

    pass
