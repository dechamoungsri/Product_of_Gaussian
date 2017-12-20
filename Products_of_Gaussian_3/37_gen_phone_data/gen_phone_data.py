
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    all_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/syllable_database/02_add_stress_database_07_nov/dict_version.pkl')

    out_dict = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/phone_level_dict/all.pkl'

    # print all_dict

    posyl = ['consonant', 'vowel', 'finalconsonant']

    phone_list = dict()

    for syl in all_dict:
        data = all_dict[syl]
        # print data

        raw_lf0 = data['raw_lf0']
        dur = data['dur']

        # print raw_lf0, dur

        frame_dur = np.array(dur) / 50000
        # print frame_dur

        base = 0

        for i in xrange( len(frame_dur) ):

            phone = dict()
            phone['phone'] = data[posyl[i]]
            phone['phone_type'] = posyl[i]
            phone['tone'] = data['tone']
            phone['stress'] = data['stress']

            phone['raw_lf0'] = data['raw_lf0'][ base : base + int(frame_dur[i]) ]

            base = base + int(frame_dur[i]) 

            # print int(frame_dur[i])

            phone['id'] = '{}_{}'.format(data['id'], i)

            # print phone
            # print phone['raw_lf0']

            phone_list[phone['id']] = phone
            
            pass

        # sys.exit()
    Utility.save_obj(phone_list, out_dict)

    pass
