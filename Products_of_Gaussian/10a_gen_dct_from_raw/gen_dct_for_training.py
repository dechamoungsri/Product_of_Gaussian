
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('/work/w21/decha/Interspeech_2017/Products_of_Gaussian/')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

from numpy.linalg import inv

if __name__ == '__main__':

    num_coeff = 3

    syl_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_dct_3_stress_coeff.pkl')

    outpath = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/dct/{}-coeff/tsc/sd/'.format(num_coeff)
    Utility.make_directory(outpath)

    label_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/'
    for s in Utility.char_range('a', 'z'):
        set_label_path = '{}/{}/'.format(label_path, s)

        set_dct_path = '{}/{}/'.format(outpath, s)
        Utility.make_directory(set_dct_path)

        for x in range(1, 51):

            name = 'tscsd{}{}'.format(s, Utility.fill_zero(x, 2))

            file_path = '{}/{}.lab'.format(set_label_path, name)
            
            if not Utility.is_file_exist(file_path): continue

            dur_list, names = PoGUtility.gen_dur_and_name_list(file_path, name)

            if len(dur_list) != len(names):
                print name

            # print names

            dct_list = []

            for n in names:
                if n in syl_dict:
                    dct_list.append(syl_dict[n])
                else:
                    dct_list.append(num_coeff*[0])

            dct_list = np.array(dct_list)

            dct_path = '{}/{}.npy'.format(set_dct_path, name)

            np.save(dct_path, dct_list)

            # sys.exit()

    pass
