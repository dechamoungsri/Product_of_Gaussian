
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

def run_cal_distortion(basename, tmp_path, predictive, alpha, beta):

    for num in range(1, 51):

        name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    
        predicted_mean_path = '{}/{}/mean.npy'.format(predictive, name)

        mean = np.load(predicted_mean_path)[:,0]

        vuv = np.load('{}/{}.npy'.format(vuv_path, name))
        vuv = vuv.reshape(len(vuv))

        mean[np.where(vuv==-1.00000000e+10)] = -1.00000000e+10

        Utility.write_to_file_line_by_line('{}/{}.lf0'.format(tmp_path, name), mean)

    rmse, l = Distortion.lf0_distortion_syn_is_readable(org_path, tmp_path)

    print 'Alpha {}, Beta {}, LF0 RMSE: {:f} in {} frames'.format(alpha, beta, rmse, l)

    pass

if __name__ == '__main__':

    predictive = '/work/w21/decha/Interspeech_2017/Result/03_Given_syllable_dct_with_weigth/num_dct_cov_7/'
    
    org_path = '/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/'

    tmp_path = './tmp2/'

    Utility.make_directory(tmp_path)

    basename = 'tscsdj'

    vuv_path = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/'

    for alpha in np.arange(1.0, 1.1, 0.1):
        for beta in np.arange(0.01,0.1,0.01):

            alpha_beta_path = '{}/alpha_{}_beta_{}/'.format(predictive, alpha, beta)

            if Utility.is_dir_exists(alpha_beta_path):
                run_cal_distortion(basename, tmp_path, alpha_beta_path, alpha, beta)

    pass
