
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

def mix_data(datafile):
    for data in Utility.load_obj(datafile):
        lf0 = data['TF']['intepolate151']['data'][0:50]
        # print lf0, len(lf0)

        delta_lf0 = data['TF']['intepolate151']['data'][50:100]
        # print delta_lf0, len(delta_lf0)

        delta_delta_lf0 = data['TF']['intepolate151']['data'][100:150]
        # print delta_delta_lf0, len(delta_delta_lf0)

        iden = data['id']

        syllable[iden] = [lf0, delta_lf0, delta_delta_lf0]

        # if data['id'] == 'tscsda39_2':
        #     print data

        # sys.exit()

if __name__ == '__main__':

    syllable = dict()

    outpath_file = '/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_data_with_delta_deltadelta.pkl'

    base = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/'

    for tone in [0,1,2,3,4]:
        for vowel in ['long', 'short']:
            for final in ['nasal', 'non-nasal', 'no']:

                name = '{}_{}_{}'.format(tone, vowel, final)
                datafile = '{}/{}.npy'.format(base, name)

                print datafile

                if Utility.is_file_exist(datafile):

                    mix_data(datafile)

                    # sys.exit()

    Utility.save_obj(syllable, outpath_file)

    pass
