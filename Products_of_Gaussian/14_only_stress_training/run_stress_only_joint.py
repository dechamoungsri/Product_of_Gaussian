
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

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

def lf0_gen_with_vuv(lf0, vuv_list):
    unvoice = np.where(vuv_list==-1)[0]
    lf0[unvoice] = unvoice_value

    return lf0

def cal_lf0(config):

    base_path = config['base_path']
    label_path = config['label_path']
    name = config['name']
    outfilepath = config['outfilepath']
    var_path = config['var_path']
    syllable_base_path = config['syllable_base_path']
    syllable_var_path = config['syllable_var_path']
    original = config['original']
    koriyama_gen = config['koriyama_gen']
    figure_path = config['figure_path']
    ph_in_syl_object_path = config['phone_in_syllable_object_path']
    stress = config['stress']
    original_vuv = config['original_vuv']

    p_in_s_file = Utility.load_obj(ph_in_syl_object_path)

    vuv = np.load('{}/class.npy'.format(config['vuv_path']))
    # vuv = original_vuv

    #--------Frame-------#

    lf0_mean = np.load('{}/mean.npy'.format(base_path))
    lf0_cov = np.load('{}/cov.npy'.format(base_path))

    var = np.load('{}'.format(var_path))

    if len(lf0_cov) > len(vuv):
        for i in range(len(lf0_cov)-len(vuv)):
            vuv.append(-1, axis=0)
    elif len(lf0_cov) < len(vuv):
        vuv = vuv[0:len(lf0_cov)]

    lf0_var = np.sum(var, axis=0)

    lf0_mean = np.array( [ lf0_mean[:,0], lf0_mean[:,1], lf0_mean[:,2] ] )
    lf0_w = PoGUtility.generate_W_for_GPR_generate_features(len(lf0_cov), vuv)

    frame_B = alpha * PoGUtility.cal_sum_of_mean_part(lf0_var, lf0_w, lf0_cov, lf0_mean)
    frame_A = alpha * PoGUtility.cal_sum_of_weight_part(lf0_var, lf0_w, lf0_cov)

    L = linalg.cholesky(frame_A, lower=True)
    lf0 = linalg.cho_solve((L, True) , frame_B)

    # lf0 = lf0_gen_with_vuv(lf0, vuv)
    print lf0.shape

    frame_lf0_nomask = np.copy(lf0) 

    # lf0 = lf0_gen_with_vuv(lf0, vuv)

    lf0[lf0<1] = np.nan

    frame_lf0 = np.copy(lf0) 

    #----------Syllable level--------#

    dur_list, names = PoGUtility.gen_dur_and_name_list(label_path, name)

    # print np.sum(dur_list)
    if np.sum(dur_list) < len(original):
        dur_list[0] = dur_list[0] + len(original)-np.sum(dur_list)
    # print np.sum(dur_list)

    syl_mean = np.load('{}/mean.npy'.format(syllable_base_path))
    syl_cov = np.load('{}/cov.npy'.format(syllable_base_path))

    s_mean = syl_mean

    var = np.load('{}'.format(syllable_var_path))
    syl_var = np.sum(var, axis=0)

    temp_mean = []
    for i in range( len(syl_mean[0]) ):
        temp_mean.append( syl_mean[:,i] )
    syl_mean = np.array(temp_mean)

    syl_w = PoGUtility.generate_DCT_W_without_consonant_on_stress(len(lf0_cov), dur_list, num_coeff, p_in_s_file, stress)

    syl_B = beta * PoGUtility.cal_sum_of_mean_part(syl_var, syl_w, syl_cov, syl_mean)
    syl_A = beta * PoGUtility.cal_sum_of_weight_part(syl_var, syl_w, syl_cov)

    #----------Combine Model--------#

    L = linalg.cholesky(frame_A + syl_A, lower=True)
    lf0 = linalg.cho_solve((L, True) , frame_B + syl_B)

    # print lf0.shape

    lf0[lf0<1] = np.nan

    PlotUtility.plot([lf0, original, frame_lf0_nomask], ['Multi', 'original', 'Single'], '{}/{}_no_mask.eps'.format(figure_path, name))

    lf0 = lf0_gen_with_vuv(lf0, vuv)
    lf0[lf0<1] = np.nan

    frame_lf0 = lf0_gen_with_vuv(frame_lf0, vuv)
    frame_lf0[frame_lf0<1] = np.nan
    
    np.save(outfilepath, lf0)

    print min(lf0)

    PlotUtility.plot([lf0, original, frame_lf0], ['Multi', 'original', 'Single'], '{}/{}_multi.eps'.format(figure_path, name))

    #----------Combine Model--------#

    o = []
    for data_dct, dur in zip(s_mean, dur_list):
        i_dct = PoGUtility.generate_inverse_DCT(data_dct, dur)
        o = o + i_dct

    o = np.concatenate(
        (np.zeros(len(original)-len(o)), 
                 np.array(o)) , axis=0)

    o = lf0_gen_with_vuv(o, vuv)
    o[o<=1] = np.nan
    # print o.shape

    PlotUtility.plot([o, original, lf0, frame_lf0], ['dct', 'original', 'Multi', 'frame_lf0'], '{}/{}_dct.eps'.format(figure_path, name))

    pass

if __name__ == '__main__':

    unvoice_value = -1.00000000e+10

    alpha = 1.0
    beta = 1.0

    increment = 0.1
    start = 0.1
    end = 4.0

    num_coeff = 3
    block_size = 256

    method = '04a_stress_only_predicted_vuv'

    outname = '/work/w21/decha/Interspeech_2017/Result/{}_block_{}/'.format(method, block_size)

    syllable_predicted_dct_path = '/work/w21/decha/Interspeech_2017/Speech_synthesis/04_syllable_level_3_dct/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-{}/B-{}/num_iters-5/dur/predictive_distribution/'.format(block_size, block_size)

    original_path = '/work/w2/decha/Data/GPR_speccom_data/data_before_remove_silence/lf0/tsc/sd/j/'

    koriyama_gen_path = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/'

    syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono/tsc/sd/j/'

    phone_in_syllable_object_path = '/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/j/'

    frame_predicted_lf0_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05a_GPR/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/lf0/predictive_distribution/'

    stress_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'

    vuv_predicted_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/05a_GPR/testrun/out/tsc/a-i/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/vuv/predictive_distribution/'

    basename = 'tscsdj'

    for b in np.arange(start, end, increment):

        beta = b

        print 'Beta : ', b

        outbase = '{}/num_dct_cov_{}/'.format(outname, num_coeff)
        outpath = '{}/Beta_{}/lf0/'.format(outbase, beta)
        figure_path = '{}/Beta_{}/fig/'.format(outbase, beta)

        Utility.make_directory(outpath)
        Utility.make_directory(figure_path)

        for num in range(1, 51):

            name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    

            print name

            outfile = '{}/{}.npy'.format(outpath, name)
            # Utility.make_directory(outfilepath)

            base_path = '{}/{}/'.format( frame_predicted_lf0_path, name )
            label_path = '{}/{}.lab'.format( syl_duration_path, name )

            var_path = '{}/inv_dimension_cov.npy'.format(frame_predicted_lf0_path)

            syllable_base_path = '{}/{}/'.format( syllable_predicted_dct_path, name )

            syllable_var_path =  '{}/inv_dimension_cov.npy'.format( syllable_predicted_dct_path )

            vuv_path = '{}/{}/'.format( vuv_predicted_path, name )

            original = Utility.read_lf0_into_ascii('{}/{}.lf0'.format(original_path, name))
            original = np.array(original)

            original_vuv = np.copy(original)
            original_vuv[original_vuv<0] = -1
            original_vuv[original_vuv>=0] = +1

            original[original<0] = np.nan

            koriyama_gen = np.load('{}/{}.npy'.format(koriyama_gen_path, name))
            koriyama_gen[koriyama_gen<0] = np.nan

            stress = '{}/{}.npy'.format(stress_path, name)
            stress = np.load(stress)

            config = {
                'base_path' : base_path,
                'label_path' : label_path,
                'name' : name,
                'outfilepath' : outfile,
                'var_path' : var_path, 
                'syllable_base_path': syllable_base_path,
                'syllable_var_path' : syllable_var_path,
                'vuv_path' : vuv_path,
                'original' : original,
                'koriyama_gen' : koriyama_gen,
                'figure_path' : figure_path,
                'phone_in_syllable_object_path': '{}/{}.dur'.format(phone_in_syllable_object_path, name),
                'stress': stress,
                'original_vuv': original_vuv
            }

            cal_lf0(config)

            # sys.exit()

    pass
