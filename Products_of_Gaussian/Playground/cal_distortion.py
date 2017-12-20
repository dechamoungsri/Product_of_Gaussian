
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    org_path = '/work/w2/decha/Data/GPR_speccom_data/full_time/tsc/sd/j/'
    org_syn_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/j/'

    outpath = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Result/alpha_1.0/450/'

    Distortion.duration_distortion_from_numpy_list(org_path, outpath)
    Distortion.duration_distortion_from_numpy_list_syllable_level(org_syn_path, outpath)

    pass
