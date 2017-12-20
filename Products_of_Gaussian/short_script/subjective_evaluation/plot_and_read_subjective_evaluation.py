
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility
from tool_box.subjective_evaluation_util.subjective_utility import SubjectiveUtility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    score_path = '/home/h1/decha/Dropbox/ICASSP_2017/icassp_2017_subjective_result/'
    SubjectiveUtility.read_mos(score_path)
    SubjectiveUtility.read_pref(score_path)

    pass
