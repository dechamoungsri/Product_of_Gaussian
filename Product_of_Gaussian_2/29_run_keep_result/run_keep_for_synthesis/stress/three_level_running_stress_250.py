
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../../../../Products_of_Gaussian/')

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

import os
import sklearn, sklearn.metrics

import numpy

import itertools

import argparse

import subprocess
import datetime

from time import gmtime, strftime

if __name__ == '__main__':

    outpath = sys.argv[1]

    block_size = 256
    training_size = 250
    num_coeff = 3
    mainoutpath = '/29_script/Exp_syn_stress/'
    syllable_predicted_path = '/work/w21/decha/Interspeech_2017/Speech_synthesis/05_syllable_level_3_dct_no_zeroth/testrun/out_all/tsc/'
    zero_coeff_path = '/work/w21/decha/Interspeech_2017/Speech_synthesis/06_zeroth_coeff_run_tree_05/testrun/out_all/tsc/'
    stress_or_unstress = 'stress'

    stress_optimal_list = [
        {
            'tone' : 0,
            'startbeta' : 2.9, 'endbeta' : 3.0,
            'startgamma' : 0.0, 'endgamma' : 0.1,
        }, 
        {
            'tone' : 1,
            'startbeta' : 0.1, 'endbeta' : 0.2,
            'startgamma' : 0.0, 'endgamma' : 0.1,
        }, 
        {
            'tone' : 2,
            'startbeta' : 1.1, 'endbeta' : 1.2,
            'startgamma' : 0.0, 'endgamma' : 0.1,
        }, 
        {
            'tone' : 3,
            'startbeta' : 1.1, 'endbeta' : 1.2,
            'startgamma' : 0.1, 'endgamma' : 0.2,
        }, 
        {
            'tone' : 4,
            'startbeta' : 1.7, 'endbeta' : 1.8,
            'startgamma' : 0.9, 'endgamma' : 1.0,
        }
    ]

    for config in stress_optimal_list:

        print config

        f = open("{}/log.{}.{}.{}.txt".format(outpath, config['tone'], training_size, datetime.datetime.now().time()), "w")

        p = subprocess.call(['/usr/local/bin/python', '-u', 'run_joint_main_three_optimal.py', 
            '-startbeta', '{}'.format(config['startbeta']),
            '-endbeta', '{}'.format(config['endbeta']), 
            '-startgamma', '{}'.format(config['startgamma']), 
            '-endgamma', '{}'.format(config['endgamma']), 
            '-stress_or_unstress', '{}'.format(stress_or_unstress), 
            '-num_coeff', '{}'.format(num_coeff), 
            '-block_size', '{}'.format(block_size), 
            '-training_size', '{}'.format(training_size), 
            '-tone', '{}'.format(config['tone']), 
            '-mainoutpath', '{}'.format(mainoutpath), 
            '-syllable_predicted_path', '{}'.format(syllable_predicted_path), 
            '-zero_coeff_path', '{}'.format(zero_coeff_path), 
            ], stdout=f)

        # output = p.stdout.readlines()
        # print output

    pass
