
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

import subprocess

if __name__ == '__main__':

    increment = 0.1

    data_dict = dict()
    data_dict['initial'] = {
        0 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 20.0, 'start_syl_0': 0.0 },
        1 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 5.6, 'start_syl_1toN': 0.0, 'start_syl_0': 1.5 },
        2 : { 'start_ph_1toN' : 6.3, 'start_ph_0': 0.0, 'start_syl_1toN': 0.0, 'start_syl_0': 0.0 },
        3 : { 'start_ph_1toN' : 0.6, 'start_ph_0': 0.0, 'start_syl_1toN': 11.5, 'start_syl_0': 0.0 },
        4 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 20.0, 'start_syl_1toN': 20.0, 'start_syl_0': 0.0 }
    }
    data_dict['vowel'] = {
        0 : { 'start_ph_1toN' : 0.5, 'start_ph_0': 0.0, 'start_syl_1toN': 6.3, 'start_syl_0': 0.0 },
        1 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 15.6, 'start_syl_1toN': 0.7, 'start_syl_0': 0.0 },
        2 : { 'start_ph_1toN' : 1.1, 'start_ph_0': 0.0, 'start_syl_1toN': 1.4, 'start_syl_0': 0.0 },
        3 : { 'start_ph_1toN' : 5.1, 'start_ph_0': 0.3, 'start_syl_1toN': 0.3, 'start_syl_0': 0.0 },
        4 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 1.9, 'start_syl_0': 1.3 }
    }
    data_dict['final'] = {
        0 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.2, 'start_syl_1toN': 0.0, 'start_syl_0': 0.2 },
        1 : { 'start_ph_1toN' : 6.1, 'start_ph_0': 6.1, 'start_syl_1toN': 0.0, 'start_syl_0': 0.2 },
        2 : { 'start_ph_1toN' : 6.1, 'start_ph_0': 0.0, 'start_syl_1toN': 0.2, 'start_syl_0': 0.0 },
        3 : { 'start_ph_1toN' : 6.1, 'start_ph_0': 6.1, 'start_syl_1toN': 2.0, 'start_syl_0': 0.2 },
        4 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 1.2, 'start_syl_1toN': 0.0, 'start_syl_0': 1.2 }
    }

    # data_dict['vowel'] = {
    #     0 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 0.0, 'start_syl_0': 0.0 },
    #     1 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 0.0, 'start_syl_0': 0.0 },
    #     2 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 0.0, 'start_syl_0': 0.0 },
    #     3 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 0.0, 'start_syl_0': 0.0 },
    #     4 : { 'start_ph_1toN' : 0.0, 'start_ph_0': 0.0, 'start_syl_1toN': 0.0, 'start_syl_0': 0.0 }
    # }

    output = []
    Utility.make_directory('./log/')
    outpath = './log/log_run_for_check_overall_result_24_May_2017.txt'

    for phone_type in ['initial', 'vowel', 'final']:
        for tone in [0,1,2,3,4]:

            process = subprocess.Popen([
                '/usr/local/bin/python', '-u', './run.py',
                '-method_name', 'Stress_Method_C_phone_syllable_tone_separated',
                '-mainoutpath', '/work/w21/decha/Interspeech_2017/Result_4/',

                '-start_ph_1toN', str(data_dict[phone_type][tone]['start_ph_1toN']), '-end_ph_1toN', str(data_dict[phone_type][tone]['start_ph_1toN']),
                '-start_ph_0', str(data_dict[phone_type][tone]['start_ph_0']), '-end_ph_0', str(data_dict[phone_type][tone]['start_ph_0']),
                '-start_syl_1toN', str(data_dict[phone_type][tone]['start_syl_1toN']), '-end_syl_1toN', str(data_dict[phone_type][tone]['start_syl_1toN']),
                '-start_syl_0', str(data_dict[phone_type][tone]['start_syl_0']), '-end_syl_0', str(data_dict[phone_type][tone]['start_syl_0']), 

                '-increment', str(increment),
                '-phone_type', phone_type,
                '-training_size', str(250),
                '-tone', str(tone),
                '-stress_type', str(1), 
                '-tone_folder', 'all',
                '-is_save_object'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            output.append(process.stdout.read())

            # print(process.stdout.read())

    Utility.write_to_file_line_by_line(outpath, output)

# /usr/local/bin/python -u ./run.py \
# -method_name Stress_Method_C_phone_syllable_tone_separated \
# -mainoutpath /work/w21/decha/Interspeech_2017/Result_3/ \
# -start_ph_1toN 0.5 -end_ph_1toN 2.0 \
# -start_ph_0 0.0 -end_ph_0 0.0 \
# -start_syl_1toN 5.5 -end_syl_1toN 10.0 \
# -start_syl_0 0.0 -end_syl_0 0.0 \
# -increment 0.1 \
# -phone_type $phone_type \
# -training_size 250 -tone $tone -stress_type 1 -tone_folder all >! ./$log/log_ph_C_tone_$tone'_c.txt'

    pass
