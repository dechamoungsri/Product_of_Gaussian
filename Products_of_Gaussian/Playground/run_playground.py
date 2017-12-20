
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    dct = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/dct_separated_tone/include_zero_coeff/all/3-coeff/tsc/sd/a/tscsda01.npy'

    print np.load(dct)

    pass
