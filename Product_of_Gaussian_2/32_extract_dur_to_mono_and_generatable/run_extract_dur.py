
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../../Products_of_Gaussian/')

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

import getopt

import os
import sklearn, sklearn.metrics

import numpy

def gen_mono(path, mono, mono_to_syl, mono_outfile, syl_outfile):

    dur = np.load(path)
    lab = Utility.read_file_line_by_line(mono)
    m_to_s = np.array( Utility.load_obj(mono_to_syl) )

    print dur.shape, m_to_s.shape

    # print m_to_s

    start = 0
    end = 0

    new_mono = []
    new_syl = []

    all_dur = 0.0

    for d, line in zip(dur, lab):
        # print d, line
        l = Utility.trim(line)
        spl = l.split(' ')

        end = int(start+d*10000000)

        o = '{} {} {}'.format(int(start), end, spl[2])
        # print o
        new_mono.append(o)

        start = end

        all_dur = all_dur + d

    start_idx = 0
    start = 0
    end = 0
    for syl in m_to_s:
        phs = len(syl)
        # print phs
        syl_dur = 0
        for d in dur[start_idx:start_idx+phs]:
            syl_dur = syl_dur + d
            # print syl_dur

        end = int(start+syl_dur*10000000)

        spl = Utility.trim(lab[start_idx]).split(' ')

        o_syl = '{} {} {}'.format(int(start), end, spl[2])
        new_syl.append(o_syl)
        # print o_syl

        start = end
        start_idx = start_idx + phs

    print all_dur * 10000000

    Utility.write_to_file_line_by_line(mono_outfile, new_mono)
    Utility.write_to_file_line_by_line(syl_outfile, new_syl)

    pass

if __name__ == '__main__':

    UNDEF_VALUE = -1.00000000e+10

    dur_path = '/work/w2/decha/Data/GPR_speccom_data/Generated_Parameter/950_GPR/dur/param_mean/'

    mono_path = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/j/'

    mono_to_syl_path = '/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/j/'

    mono_outpath = '/work/w2/decha/Data/GPR_speccom_data/Generated_Parameter/950_GPR/mono/j/'
    Utility.make_directory(mono_outpath)

    syl_outpath = '/work/w2/decha/Data/GPR_speccom_data/Generated_Parameter/950_GPR/syllable/j/'
    Utility.make_directory(syl_outpath)

    for i in range(1, 51):
        path = '{}/tscsdj{}.npy'.format( dur_path, Utility.fill_zero(i, 2) )
        mono = '{}/tscsdj{}.lab'.format( mono_path, Utility.fill_zero(i, 2) )

        mono_to_syl = '{}/tscsdj{}.dur'.format( mono_to_syl_path, Utility.fill_zero(i, 2) )

        mono_outfile = '{}/tscsdj{}.lab'.format( mono_outpath, Utility.fill_zero(i, 2) )

        syl_outfile = '{}/tscsdj{}.lab'.format( syl_outpath, Utility.fill_zero(i, 2) )

        gen_mono(path, mono, mono_to_syl, mono_outfile, syl_outfile)

        # sys.exit()

    pass
