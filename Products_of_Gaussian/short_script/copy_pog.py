
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    ref_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05_GPR_abcdefghijklmnopqrst/testrun/out/tsc/a-t/speech_param/a-t/demo/seed-00/M-1024/B-1024/num_iters-5/dur_old/param_mean/'

    pog_path = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Result/alpha_1.0/a-i/tscsdj01_mean.npy'
    pog = np.load(pog_path).shape

    out_path = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Using_result/450_dur/'

    pog_path = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Result/alpha_1.0/a-i/'
    
    for f in Utility.list_file(pog_path):
        if f.startswith('.'): continue
        if 'mean' not in f: continue

        basename = Utility.get_basefilename(f)
        base = basename[0:len(basename)-5]
        
        pog = np.load('{}/{}'.format(pog_path, f)).shape
        ref = np.load('{}/{}.npy'.format(ref_path, base)).shape

        Utility.copyFile('{}/{}'.format(pog_path, f), '{}/{}.npy'.format(out_path, base))

    pass
