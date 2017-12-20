
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

import itertools

if __name__ == '__main__':

    coeffs = [3, 4, 7, 1]
    tones = ['all', 0, 1, 2, 3, 4]
    include_zero = ['not_include_zero_coeff', 'include_zero_coeff']

    stress_unstress = ['unstress', 'stress']

    stress_dict = {
        'stress' : 1,
        'unstress' : 0
    }

    syl_dict_path = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/phone_level_dict/all_clean.pkl'

    syl_dict = Utility.load_obj(syl_dict_path)

    # print syl_dict[syl_dict.keys()[20]], syl_dict.keys()[20]

    # sys.exit()

    for (num_coeff, tone, incl_zero, stress_type) in itertools.product(coeffs, tones, include_zero, stress_unstress):

        print (num_coeff, tone, incl_zero, stress_type) 

        # syl_dict_path = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/tone_separated/tone_{}_dct_coeff_{}.pkl'.format(tone, num_coeff)

        # outpath = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/dct_separated_tone/{}/{}/{}-coeff/tsc/sd/'.format(incl_zero, tone, num_coeff)

        outpath = '/work/w2/decha/Data/GPR_speccom_data/01_phone_level_data/dct_separated_stress_tone/{}/{}/{}/{}-coeff/tsc/sd/'.format(stress_type, incl_zero, tone, num_coeff)

        Utility.make_directory(outpath)

        print outpath

        # label_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/'
        # label_path = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/'
        label_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/'

        for s in Utility.char_range('a', 'z'):
            set_label_path = '{}/{}/'.format(label_path, s)

            set_dct_path = '{}/{}/'.format(outpath, s)
            Utility.make_directory(set_dct_path)

            for x in range(1, 51):

                name = 'tscsd{}{}'.format(s, Utility.fill_zero(x, 2))

                file_path = '{}/{}.lab'.format(set_label_path, name)
                
                if not Utility.is_file_exist(file_path): continue

                dur_list, names = PoGUtility.gen_dur_and_name_list_for_phone(file_path, name)

                # sys.exit()

                # if len(dur_list) != len(names):
                #     print name, len(dur_list), len(names)

                dct_list = []

                for n in names:

                    case = 0

                    if n in syl_dict:
                        if (tone == 'all') & ( int(syl_dict[n]['stress'])==stress_dict[stress_type] ):
                            case = 1
                        elif (tone == int(syl_dict[n]['tone'])) & ( int(syl_dict[n]['stress'])==stress_dict[stress_type] ):
                            case = 1
                        else:
                            case = 0
                    else:
                        case = 0

                    if case == 1:
                        if incl_zero == 'not_include_zero_coeff':
                            dct_list.append(syl_dict[n]['dct'][1:num_coeff])
                        else:
                            dct_list.append(syl_dict[n]['dct'][0:num_coeff])
                    else:
                        if incl_zero == 'not_include_zero_coeff':
                            dct_list.append((num_coeff-1)*[0])
                        else:
                            dct_list.append(num_coeff*[0])

                dct_list = np.array(dct_list)

                # print dct_list

                dct_path = '{}/{}.npy'.format(set_dct_path, name)

                np.save(dct_path, dct_list)

                # sys.exit()

    pass
