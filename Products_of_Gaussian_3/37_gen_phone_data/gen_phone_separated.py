
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

import itertools

if __name__ == '__main__':

    phone_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/phone_level_dict/all_clean.pkl')

    out_path = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/phone_level_dict/all_clean'

    phone_clean_dict = dict()
    coeff = 7

    stress = ['stress', 'unstress']
    tone = ['0', '1', '2', '3', '4']

    out_dict = dict()

    for s, t in itertools.product(stress, tone):
        key = '{}_tone-{}'.format(s, t)
        out_dict[key] = []

    for phone_id in phone_dict:

        phone = phone_dict[phone_id]
        # print phone

        stress = 'unstress'

        if phone['stress'] == '1':
            stress = 'stress'

        tone = phone['tone']

        out_dict['{}_tone-{}'.format(stress, tone)].append(phone)

    stress = ['stress', 'unstress']
    tone = ['0', '1', '2', '3', '4']

    for s, t in itertools.product(stress, tone):
        key = '{}_tone-{}'.format(s, t)

        print key, len(out_dict[key])

        Utility.save_obj(out_dict[key], '{}_{}.pkl'.format(out_path, key))

    pass
