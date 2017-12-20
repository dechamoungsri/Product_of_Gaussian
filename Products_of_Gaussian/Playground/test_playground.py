
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

from PoG_Utility.pog_utility import PoGUtility

if __name__ == '__main__':

    print np.load('/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/dct_separated_tone/not_include_zero_coeff/4/3-coeff/tsc/sd/a/tscsda03.npy')

    pass
