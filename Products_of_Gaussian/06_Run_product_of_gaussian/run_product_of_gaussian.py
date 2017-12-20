
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct

def gen_mean_and_cov_of_dct(names):

    mean = np.array([])

    for n in names:
        # print n
        if n in syllable_dct_dict:
            # print syllable_dct_dict[n][0:num_coeff][:,0]
            data = np.array( [syllable_dct_dict[n][0:num_coeff][:,0]] ).reshape(num_coeff,1)

        else:
            data = np.zeros((num_coeff, 1))
            # data.fill(unvoice)
            data.fill(0)
            # data = np.column_stack(
            #     (
            #         dct(data[:,0], norm='ortho'), 
            #         dct(data[:,1], norm='ortho'), 
            #         dct(data[:,2], norm='ortho')
            #     )
            # )
            # print data
            # sys.exit()

        if len(mean) == 0:
            mean = data
        else:
            mean = np.concatenate((mean, data))

    cov = np.identity(mean.shape[0])

    # print mean

    return (mean, cov)

    pass

def gen_W(number_of_frame, dur_list, num_coeff):

    w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

    offset_x = 0
    offset_y = 0

    for idx, d in enumerate(dur_list):

        if idx == (len(dur_list)-1):
            d = number_of_frame-offset_x

        local_w = PoGUtility.generate_W_for_DCT(d, num_coeff)

        # print offset_x, offset_y, local_w.shape 

        for i in range(num_coeff):
            w[offset_y+i][offset_x:offset_x+d] = local_w[i]

        offset_x = offset_x + d
        offset_y = offset_y + num_coeff

    return w

    pass

def gen_dur_and_name_list(label_path, name):
    dur_list = []
    names = []
    for idx, line in enumerate(Utility.read_file_line_by_line(label_path)):
        spl = Utility.trim(line).split(' ')

        frame = int(spl[1]) - int(spl[0])
        frame = frame/50000

        dur_list.append(frame)

        names.append('{}_{}'.format(name, (idx+1) ))

    return (dur_list, names)

def cal_PoG(config):

    base_path = config['base_path']
    label_path = config['label_path']
    name = config['name']
    outfilepath = config['outfilepath']

    #--------Frame-------#

    lf0_mean = np.load('{}/mean.npy'.format(base_path))
    lf0_cov = np.load('{}/cov.npy'.format(base_path))

    print lf0_cov

    sys.exit()

    lf0_w = PoGUtility.generate_W_for_dynamic_feature_extraction(len(lf0_mean))

    #--------Syllable-------#

    dur_list, names = gen_dur_and_name_list(label_path, name)

    syllable_w = gen_W(len(lf0_mean), dur_list, num_coeff)
    syllable_mean, syllable_cov = gen_mean_and_cov_of_dct(names)

    #--------Calculation-------#

    print lf0_w.shape, lf0_mean.shape, lf0_cov.shape
    print syllable_w.shape, syllable_mean.shape, syllable_cov.shape, 

    # lf0_inv_P = PoGUtility.cal_invert_P(lf0_w, lf0_cov)
    # lf0_R = PoGUtility.cal_R(lf0_w, lf0_cov, lf0_mean)

    syllable_inv_P = PoGUtility.cal_invert_P(syllable_w, syllable_cov)
    syllable_R = PoGUtility.cal_R(syllable_w, syllable_cov, syllable_mean)

    # mean, cov = PoGUtility.cal_product_of_gaussian(lf0_R, lf0_inv_P, syllable_R, syllable_inv_P)

    # print mean
    # print cov

    sys.exit()

    # np.save('{}/mean.npy'.format(outfilepath), mean)
    # np.save('{}/cov.npy'.format(outfilepath), cov)

    pass

if __name__ == '__main__':

    unvoice = -1.00000000e+10

    syllable_dct_dict = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/Interspeech2017/syllable_dct_with_delta_dictionary.pkl')

    num_coeff = 10

    syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/j/'

    frame_predicted_lf0_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05a_GPR/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/predictive_distribution/'

    basename = 'tscsdj'

    outpath = '/work/w21/decha/Interspeech_2017/Result/01_Given_syllable_dct/num_dct_cov_{}/'.format(num_coeff)
    Utility.make_directory(outpath)

    for num in range(1, 51):

        name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    

        outfilepath = '{}/{}/'.format(outpath, name)
        Utility.make_directory(outfilepath)

        base_path = '{}/{}/'.format( frame_predicted_lf0_path, name )
        label_path = '{}/{}.lab'.format( syl_duration_path, name )

        config = {
            'base_path' : base_path,
            'label_path' : label_path,
            'name' : name,
            'outfilepath' : outfilepath
        }

        cal_PoG(config)

        # sys.exit()

    pass
