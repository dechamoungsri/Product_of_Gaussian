
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import re

import sklearn, sklearn.metrics

if __name__ == '__main__':

    path = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Result/alpha_1.0/450/'

    print path

    original_path = '/work/w2/decha/Data/GPR_speccom_data/full_time/tsc/sd/j/'

    ori = []
    ph_list = []

    syn = []

    for f in Utility.list_file(path):
        if f.startswith('.'): continue
        if 'mean' not in f : continue

        syn_path = '{}/{}'.format(path, f)
        # print syn_path
        syn_list = np.load(syn_path)
        sl = syn_list.flatten()
        syn.extend(list(sl))

        base = Utility.get_basefilename(f)
        base = base[0:len(base)-5]
        ori_path = '{}/{}.lab'.format(original_path, base)
        # print ori_path

        phone_list, dur_list = load_ori_list_in_sec(ori_path)

        ori.extend(dur_list)
        ph_list.extend(phone_list)

    print len(ph_list), len(ori), len(syn)

    dur_true_list = []
    dur_pred_list = []

    for idx, p in enumerate( ph_list ):
        if (p == 'sil') | (p == 'pau') : continue

        dur_true_list.append(1000 * ori[idx] )
        dur_pred_list.append(1000 * syn[idx] )

    if len(dur_true_list) != len(dur_pred_list):
        print "Not equal"
        
    rmse = np.sqrt(sklearn.metrics.mean_squared_error(dur_true_list, dur_pred_list))
    print('Duration RMSE: {:f} in {} phones'.format(rmse, len(dur_true_list)))

    pass
