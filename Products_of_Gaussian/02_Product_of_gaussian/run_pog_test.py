
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    alpha = 1.0

    sets = ['a','c','e','g','i','l','n','p','r','t']
    end_set = 'i'

    org_path = '/work/w2/decha/Data/GPR_speccom_data/full_time/tsc/sd/j/'

    org_syn_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/j/'

    file_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/j/'

    syl_dist_path = '/work/w15/decha/decha_w15/Specom_w15/02_GPR_syllable_level_remove_silience/testrun/out/tsc/a-{}/infer/a-{}/demo/seed-00/M-1024/B-1024/num_iters-5/dur/predictive_distribution/'.format(end_set, end_set)

    ph_dist_path = '/work/w15/decha/decha_w15/Specom_w15/05b_GPR_for_duration/testrun/out/tsc/a-{}/infer/a-{}/demo/seed-00/M-1024/B-1024/num_iters-5/dur/predictive_distribution/'.format(end_set, end_set)

    # outpath = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Result/alpha_{}_beta_{}/a-{}/'.format(alpha, beta, end_set)

    # Utility.make_directory(outpath)

    for f in Utility.list_file(file_path):
        label_file = '{}/{}'.format(file_path, f)
        w = PoGUtility.read_file_to_W(label_file)

        base = Utility.get_basefilename(f)

        syl_predictive_dist_path = '{}/{}/'.format(syl_dist_path, base)
        syllable_mean, syllable_cov = PoGUtility.read_mean_and_cov_of_predictive_distribution(syl_predictive_dist_path)

        ph_predictive_dist_path = '{}/{}/'.format(ph_dist_path, base)
        phone_mean, phone_cov = PoGUtility.read_mean_and_cov_of_predictive_distribution(ph_predictive_dist_path)

        print w.shape, syllable_mean.shape, syllable_cov.shape, phone_mean.shape, phone_cov.shape

        mean, cov = PoGUtility.cal_mean_variance_of_product_of_gaussian(w, syllable_mean, syllable_cov, phone_mean, phone_cov)

        sys.exit()


    pass
