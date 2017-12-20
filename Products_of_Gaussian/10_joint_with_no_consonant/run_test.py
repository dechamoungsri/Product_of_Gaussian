
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    frame_less_count = 0

    count = 0

    for t in [0,1,2,3,4]:
        for l in ['short', 'long']:
            for n in ['no', 'nasal', 'non-nasal']:

                path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/{}_{}_{}.npy'.format(t, l, n)

                if Utility.is_file_exist(path):

                    syl_dict = Utility.load_obj(path)

                    for s in syl_dict: 

                        syl = s

                        dur = 0.0
                        for i, d in enumerate(syl['dur']):
                            if i == 0: continue
                            dur = dur + float(d)

                        # print dur 
                        # print syl['dur']
                        frame = dur/50000.0

                        if frame < 10:
                            frame_less_count += 1

                        count+=1


    print 'frame_less_count : ', frame_less_count, count

    pass
