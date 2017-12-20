
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct
from numpy.linalg import inv

def cal_lf0(config):

    base_path = config['base_path']
    label_path = config['label_path']
    name = config['name']
    outfilepath = config['outfilepath']
    var_path = config['var_path']

    #--------Frame-------#

    lf0_mean = np.load('{}/mean.npy'.format(base_path))
    lf0_cov = np.load('{}/cov.npy'.format(base_path))

    var = np.load('{}'.format(var_path))
    vv = []
    for i, v in enumerate(var):
        vv.append(v[i])

    var = np.array(vv)

    lf0_mean = np.array( [ lf0_mean[:,0], lf0_mean[:,1], lf0_mean[:,2] ] )
    lf0_w = PoGUtility.generate_W_for_GPR_generate_features(len(lf0_cov))

    B = PoGUtility.cal_sum_of_mean_part(var, lf0_w, lf0_cov, lf0_mean)
    A = PoGUtility.cal_sum_of_weight_part(var, lf0_w, lf0_cov)

    lf0 = np.dot( inv(A), B )

    print lf0.shape

    np.save(outfilepath, lf0)

    sys.exit()

    pass

if __name__ == '__main__':

    unvoice = -1.00000000e+10

    syllable_dct_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dct_with_delta_dictionary.pkl')

    num_coeff = 7

    syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/j/'

    frame_predicted_lf0_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05a_GPR/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/predictive_distribution/'

    basename = 'tscsdj'

    outpath = '/work/w21/decha/Interspeech_2017/Result/01_Given_syllable_dct_Joint_probability/num_dct_cov_{}/'.format(num_coeff)
    Utility.make_directory(outpath)

    for num in range(1, 51):

        name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    

        outfile = '{}/{}.npy'.format(outpath, name)
        # Utility.make_directory(outfilepath)

        base_path = '{}/{}/'.format( frame_predicted_lf0_path, name )
        label_path = '{}/{}.lab'.format( syl_duration_path, name )

        var_path = '{}/inv_dimension_cov.npy'.format(frame_predicted_lf0_path)

        config = {
            'base_path' : base_path,
            'label_path' : label_path,
            'name' : name,
            'outfilepath' : outfile,
            'var_path' : var_path
        }

        cal_lf0(config)

        # sys.exit()

    pass
