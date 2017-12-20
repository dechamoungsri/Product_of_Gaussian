
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('/work/w21/decha/Interspeech_2017/Products_of_Gaussian/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

from PoG_Utility.pog_utility import PoGUtility

def find_head_and_tail(lf0_list):
    head_count = 0
    for v in lf0_list:
        if v<0: 
            head_count+=1
        else:
            break

    tail_count = 0
    for v in reversed(lf0_list):
        if v<0: 
            tail_count+=1
        else:
            break

    return (head_count, tail_count)

if __name__ == '__main__':

    phone_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/phone_level_dict/all.pkl')

    new_phone_dict = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/phone_level_dict/all_clean.pkl'

    phone_clean_dict = dict()

    coeff = 7

    for phone_id in phone_dict:

        phone = phone_dict[phone_id]

        # print phone

        head_count, tail_count = find_head_and_tail(phone['raw_lf0'])

        raw = np.array(phone['raw_lf0'])[head_count : len(phone['raw_lf0'])-tail_count]
        # print raw

        if len(raw) < 10:
            continue
        else:
            if len(raw[raw<0]) != 0:
                # print raw
                raw = Utility.inteporate_lf0(raw)
                # print raw
            
            phone['clean_raw'] = raw
            phone_clean_dict[phone_id] = phone

            w = PoGUtility.generate_W_for_DCT(len(raw), coeff)
            data_dct = np.dot(w, raw)

            # print data_dct

            phone['dct'] = data_dct

            # sys.exit()

    print len(phone_clean_dict)
    Utility.save_obj(phone_clean_dict, new_phone_dict)

    pass
