
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility
from PoG_Utility.plot_utility import PlotUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct
from numpy.linalg import inv

from sklearn.metrics.pairwise import rbf_kernel

from scipy import array, linalg, dot

import re

def gen_stress(filepath, outpath):

    # sil-l+xx/A:x_x-1_1+2_2/B:x-3+0/C:x_x-1_1+1_2/D:x-3+3/E:x-1+2/F:x_x-3_1+6_2/G:x_18_12/H:x-47+47/I:x-0+0

    out = []

    pattern = re.compile(r""".+/A:.+\-(?P<cur_phone_position>.+)_.+\+.+/B:.+\-(?P<tone>.+)\+.+/C:.+/I:.+\-(?P<stress>.+)\+.+""",re.VERBOSE)

    for line in Utility.read_file_line_by_line(filepath):
        match = re.match(pattern, line)
        if match:
           cur_phone_position = match.group('cur_phone_position')
           stress = match.group('stress')
           tone = match.group('tone')

           # print line, cur_phone_position, stress

           if cur_phone_position in ['1', 'x']:
                out.append((stress, tone))

    np.save(outpath, np.array(out))


if __name__ == '__main__':

    full_path = '/work/w2/decha/Data/GPR_speccom_data/full_with_stress/tsc/sd/'

    out_main_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/'

    for sett in Utility.char_range('a', 'z'):
        sett_path = '{}/{}/'.format(full_path, sett)

        sett_out = '{}/{}/'.format(out_main_path, sett)

        Utility.make_directory(sett_out)

        for num in range(1, 51):
            filepath = '{}/tscsd{}{}.lab'.format(sett_path, sett, Utility.fill_zero(num, 2) )

            if not Utility.is_file_exist(filepath) : continue

            outfile = '{}/tscsd{}{}.npy'.format(sett_out, sett, Utility.fill_zero(num, 2) )

            gen_stress(filepath, outfile)

            # sys.exit()

    pass
