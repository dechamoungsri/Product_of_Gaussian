
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

from sklearn.metrics.pairwise import rbf_kernel

def gen_mean_and_cov_of_dct_fake(names):

    mean = []

    for n in names:
        # print n
        if n in syllable_dct_dict:
            data = syllable_dct_dict[n]

        else:
            data = np.array([0] * num_coeff)

        mean.append(data)

    mean = np.array(mean)
    cov = np.random.rand(len(mean), len(mean))

    # print cov
    # print mean.shape, cov.shape

    return (mean, cov)

    pass

def cal_lf0(config):

    base_path = config['base_path']
    label_path = config['label_path']
    name = config['name']
    outfilepath = config['outfilepath']
    var_path = config['var_path']
    syllable_base_path = config['syllable_base_path']
    syllable_var_path = config['syllable_var_path']

    #----------Syllable level--------#

    dur_list, names = PoGUtility.gen_dur_and_name_list(label_path, name)
    # print dur_list
    # print names

    syl_mean = np.load('{}/mean.npy'.format(syllable_base_path))

    # syl_mean, cccc = gen_mean_and_cov_of_dct_fake(names)

    syl_cov = np.load('{}/cov.npy'.format(syllable_base_path))

    print syl_cov

    var = np.load('{}'.format(syllable_var_path))
    vv = []
    for i, v in enumerate(var):
        vv.append(v[i])
    syl_var = np.array(vv)

    o = []
    for data_dct, dur in zip(syl_mean, dur_list):
        i_dct = PoGUtility.generate_inverse_DCT(data_dct, dur)
        # print i_dct
        o = o + i_dct

    o = np.array(o)
    o[o<3] = np.nan
    print o.shape

    org = Utility.read_lf0_into_ascii('/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/{}.lf0'.format(name))

    org[org<0] = np.nan

    diff = len(org)-len(o)

    plt.plot(np.arange(len(o))+diff, o, label='syn')
    plt.plot(range(len(org)), org, label='org')

    plt.legend()
    plt.savefig('./{}_dct_16_test.eps'.format(name))

    sys.exit()

    pass

if __name__ == '__main__':

    unvoice = -1.00000000e+10

    alpha = 1.0
    beta = 1.0

    syllable_dct_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dictionary_dct_given_mean.pkl')

    num_coeff = 7

    syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/j/'

    frame_predicted_lf0_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05a_GPR/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/predictive_distribution/'

    syllable_predicted_dct_path = '/work/w21/decha/Interspeech_2017/Speech_synthesis/01_syllable_level/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-16/B-16/num_iters-5/dur/predictive_distribution/'

    basename = 'tscsdj'

    outpath = '/work/w21/decha/Interspeech_2017/Result/01_Given_syllable_model_combined/num_dct_cov_{}/'.format(num_coeff)
    Utility.make_directory(outpath)

    for num in range(1, 51):

        name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    

        outfile = '{}/{}.npy'.format(outpath, name)
        # Utility.make_directory(outfilepath)

        base_path = '{}/{}/'.format( frame_predicted_lf0_path, name )
        label_path = '{}/{}.lab'.format( syl_duration_path, name )

        var_path = '{}/inv_dimension_cov.npy'.format(frame_predicted_lf0_path)

        syllable_base_path = '{}/{}/'.format( syllable_predicted_dct_path, name )

        syllable_var_path =  '{}/inv_dimension_cov.npy'.format( syllable_predicted_dct_path )

        config = {
            'base_path' : base_path,
            'label_path' : label_path,
            'name' : name,
            'outfilepath' : outfile,
            'var_path' : var_path, 
            'syllable_base_path': syllable_base_path,
            'syllable_var_path' : syllable_var_path
        }

        cal_lf0(config)

        # sys.exit()

    pass
