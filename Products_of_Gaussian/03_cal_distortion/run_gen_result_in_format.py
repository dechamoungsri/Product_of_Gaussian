
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

if __name__ == '__main__':

    predictive = '/work/w21/decha/Interspeech_2017/Result/03_Given_syllable_dct_use_mean_as_unvoice/num_dct_cov_7/'
    
    outpath = '/work/w21/decha/Interspeech_2017/Result/From_03_with_mean_as_unvoice_lf0_format/num_dct_cov_7/'

    # predictive = '/work/w21/decha/Interspeech_2017/GPR_data/450/predictive_distribution_align/lf0/predictive_distribution/'

    # outpath = '/work/w21/decha/Interspeech_2017/Result/From_00_lf0_format/num_dct_cov_10/'

    # predictive = '/work/w21/decha/Interspeech_2017/Result/01_Given_syllable_dct/num_dct_cov_10/'
    # outpath = '/work/w21/decha/Interspeech_2017/Result/From_01_lf0_format/num_dct_cov_10/'

    # predictive = '/work/w21/decha/Interspeech_2017/Result/02_Given_syllable_dct_without_delta/num_dct_cov_7/'
    # outpath = '/work/w21/decha/Interspeech_2017/Result/From_02_lf0_format/num_dct_cov_7/'

    Utility.make_directory(outpath)

    basename = 'tscsdj'

    vuv_path = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/'

    # pre_lf0 = '/work/w21/decha/Interspeech_2017/GPR_data/450/predictive_distribution_align/lf0/predictive_distribution/tscsdj01/mean.npy'

    # print np.load(pre_lf0)[1594]

    for num in range(1, 51):

        name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    
        predicted_mean_path = '{}/{}/mean.npy'.format(predictive, name)

        mean = np.load(predicted_mean_path)[:,0]

        vuv = np.load('{}/{}.npy'.format(vuv_path, name))
        vuv = vuv.reshape(len(vuv))

        # print vuv[1594]

        mean[np.where(vuv==-1.00000000e+10)] = -1.00000000e+10

        # print mean[1594]

        Utility.write_to_file_line_by_line('{}/{}.lf0'.format(outpath, name), mean)

        # sys.exit()

    pass
