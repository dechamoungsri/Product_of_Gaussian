
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    syllable_label_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/syllable_time/'

    count = 0

    for sett in Utility.char_range('a', 'i'):
        path = '{}/{}/'.format(syllable_label_path, sett)
        for filee in Utility.list_file(path):
            for l in Utility.read_file_line_by_line('{}/{}'.format(path, filee)):
                if 'sil' in l : continue
                if 'pau' in l : continue
                count = count + 1


    print count

    pass
