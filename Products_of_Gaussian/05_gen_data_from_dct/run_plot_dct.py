
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import idct

if __name__ == '__main__':

    unvoice = -1.00000000e+10

    target_file = 'tscsdj01'

    syllable_dct_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dct_with_delta_dictionary.pkl')

    label_file = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/j/tscsdj01.lab'

    org = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/tscsdj01.npy'

    org = np.load(org)

    count = 1

    for line in Utility.read_file_line_by_line(label_file):
        l = Utility.trim(line)
        spl = l.split(' ')

        dur = float(int(spl[1]) - int(spl[0]))/50000

        name = '{}_{}'.format(target_file, count)

        if name in syllable_dct_dict:
            dct = syllable_dct_dict[name][:,0]

            print dct
            print dct[0:7]
            
            lf0 = idct(dct[1:15], norm='ortho')
            print lf0

            sys.exit()

        count = count + 1


    pass
