
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

def read_rmse_file(rmse_file):

    param_old = []
    rmse_old = 100000000.0
    line_old = ''
    const = ''
    thefile = Utility.read_file_line_by_line(rmse_file)

    # print rmse_file

    for idx, line in enumerate(thefile):
        if 'const' in line:
            const = Utility.trim(line)

            l = thefile[idx+1].split(' ')
            current_param = [ l[0], l[1], l[2], l[3], l[4] ]

        if 'Only' in line:
            spl = line.split(' ')
            rmse = float(spl[5])

            if rmse < rmse_old:
                rmse_old = rmse
                param_old = current_param
                line_old = line

    return (rmse_old, param_old, line_old, const)


if __name__ == '__main__':

    # base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/40_run_gen/log/log_ph_B_tone_'
    # base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/41_run_separated_phone/log_2017_04_27/log_ph_C_tone_'
    # base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/41_run_separated_phone/log_2017_04_27_final/log_ph_C_tone_'

    # base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/41_run_separated_phone/log_2017_04_27_initial/log_ph_C_tone_'

    # base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/41_run_separated_phone/log_2017_04_28_vowel_tone_separated/log_ph_C_tone_'

    # base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/40_run_gen/log/log_ph_B_tone_'
    base = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/41_run_separated_phone/log_phone_and_syllable_2017_04_28_vowel_tone_separated/log_ph_C_tone_'

    for tone in [0, 1, 2, 3, 4]:
        rmse_file = '{}{}.txt'.format(base, tone)
        rmse, param, line, c = read_rmse_file(rmse_file)
        print 'Tone {}'.format(tone)
        print c
        print param
        print line

    rmse_file = '/work/w21/decha/Interspeech_2017/Products_of_Gaussian_3/41_run_separated_phone/log_phone_and_syllable_2017_04_28_vowel_tone_separated/log_ph_C_tone_0_4-6.txt'
    rmse, param, line, c = read_rmse_file(rmse_file)
    print c
    print param
    print line

    pass
