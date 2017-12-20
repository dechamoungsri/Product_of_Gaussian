
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import re

from numpy.linalg import inv

import math

class PlotUtility(object):

    @staticmethod
    def plot(data, label, outpath):
        plt.clf()
        fig = plt.gcf()
        fig.set_size_inches(15, 4)

        for d, lab in zip(data, label):

            plt.plot(range( len(d) ), d, label=lab)

        # plt.ylim([4.8, 6.0])
        plt.legend()
        plt.savefig(outpath)





