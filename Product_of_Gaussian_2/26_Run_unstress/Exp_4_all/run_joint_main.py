
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../../../Products_of_Gaussian/')

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
import argparse

from time import gmtime, strftime

def lf0_distortion_syn_is_gpr_format(org_path,syn_path, stress_list, mono_label):
    
    lf0_true_list = []
    lf0_pred_list = []
    
    lf0_true_stress_list = []
    lf0_pred_stress_list = []

    for base in Utility.list_file(org_path) :
        
        if base.startswith('.'):
            continue

        b = Utility.get_basefilename(base)
        stress = np.load('{}/{}.npy'.format(stress_list, b))
        mono_file = Utility.read_file_line_by_line('{}/{}.lab'.format(mono_label, b))

        stress_index = np.array([])

        for st, mono in zip(stress, mono_file):
            spl = mono.split(' ')
            start = int(spl[0])/50000
            end = int(spl[1])/50000

            if (st[0] != '1') & ( st[1] == '{}'.format(tone) ):
                stress_index = np.append(stress_index, np.arange(start, end), axis=0 )

        # Load Original
        original_file = os.path.join(org_path, base)
        original_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(original_file))
        
        # Load Synthesis
        synthesis_file = '{}/{}.npy'.format(syn_path, Utility.get_basefilename(base) )
        synthesis_vector = numpy.load(synthesis_file)
        synthesis_vector = synthesis_vector.reshape(len(synthesis_vector))

        # print synthesis_vector
        synthesis_vector = np.nan_to_num(synthesis_vector)
        synthesis_vector[ np.where(synthesis_vector<=0.0) ] = UNDEF_VALUE

        # print synthesis_vector
        # sys.exit()

        for idx, (lf0_original, lf0_synthesis )in enumerate(zip(original_vector, synthesis_vector)):
            if lf0_original == UNDEF_VALUE:
                continue
            if lf0_synthesis == UNDEF_VALUE:
                continue

            lf0_true_list.append(lf0_original)
            lf0_pred_list.append(lf0_synthesis)

            if idx in stress_index:
                lf0_true_stress_list.append(lf0_original)
                lf0_pred_stress_list.append(lf0_synthesis)

    # rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1000 / numpy.log(2)
    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
    print('All LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_stress_list, lf0_pred_stress_list)) * 1200 / numpy.log(2)
    print('Only unstress LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_stress_list)))

    pass

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
    
    if mask == 'original':
        vuv = original_vuv

    #--------Frame-------#

    lf0_mean = np.load('{}/mean.npy'.format(base_path))
    lf0_cov = np.load('{}/cov.npy'.format(base_path))
    config['number_of_frame'] = len(lf0_cov)

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
    # print lf0.shape

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

    if weight_type_of_stress=='stress':
        syl_w = PoGUtility.generate_DCT_W_without_consonant_on_stress_vuv_head_tail_tone(len(lf0_cov), dur_list, num_coeff, p_in_s_file, stress, vuv, tone)
    elif weight_type_of_stress=='unstress':
        syl_w = PoGUtility.generate_DCT_W_without_consonant_on_unstress_vuv_head_tail_tone(len(lf0_cov), dur_list, num_coeff, p_in_s_file, stress, vuv, tone)
    else:
        syl_w = PoGUtility.generate_DCT_W_without_consonant_vuv_head_tail_tone(len(lf0_cov), dur_list, num_coeff, p_in_s_file, stress, vuv, tone)

    # all coeff
    if args.use_partial_coeff :
        syl_w = syl_w[1:num_coeff]


    syl_B = beta * PoGUtility.cal_sum_of_mean_part(syl_var, syl_w, syl_cov, syl_mean)
    syl_A = beta * PoGUtility.cal_sum_of_weight_part(syl_var, syl_w, syl_cov)

    #----------Combine Model--------#

    L = linalg.cholesky(frame_A + syl_A, lower=True)
    lf0 = linalg.cho_solve((L, True) , frame_B + syl_B)

    # print lf0.shape

    lf0[lf0<1] = np.nan

    if args.plot:
        PlotUtility.plot([original, frame_lf0_nomask, lf0], ['original', 'Single', 'Multi'], '{}/{}_no_mask.eps'.format(figure_path, name))

    lf0 = lf0_gen_with_vuv(lf0, vuv)
    lf0[lf0<1] = np.nan

    frame_lf0 = lf0_gen_with_vuv(frame_lf0, vuv)
    frame_lf0[frame_lf0<1] = np.nan
    
    np.save(outfilepath, lf0)

    # print min(lf0)

    if args.plot:
        PlotUtility.plot([original, frame_lf0, lf0], ['original', 'Single', 'Multi'], '{}/{}_multi.eps'.format(figure_path, name))

    #----------Combine Model--------#

    o = []
    for data_dct, dur in zip(s_mean, dur_list):
        i_dct = PoGUtility.generate_inverse_DCT(data_dct, dur, 1)
        o = o + i_dct

    o = np.concatenate(
        (np.zeros(len(original)-len(o)), 
                 np.array(o)) , axis=0)

    # o = lf0_gen_with_vuv(o, vuv)
    # o[o<=1] = np.nan
    o = o + 5.0
    # print o.shape

    if args.plot:
        PlotUtility.plot([o, original, frame_lf0, lf0], ['dct', 'original', 'frame_lf0', 'Multi'], '{}/{}_dct.eps'.format(figure_path, name))

    pass

if __name__ == '__main__':

    unvoice_value = -1.00000000e+10

    alpha = 1.0
    beta = 1.0

    increment = 0.2

    parser = argparse.ArgumentParser()
    parser.add_argument('-startbeta')
    parser.add_argument('-endbeta')
    parser.add_argument('-plot', action='store_true')
    parser.add_argument('-stress_or_unstress')
    parser.add_argument('-use_partial_coeff', action='store_true')
    parser.add_argument('-num_coeff')
    parser.add_argument('-block_size')
    parser.add_argument('-training_size')
    parser.add_argument('-tone')
    args = parser.parse_args()

    start = float(args.startbeta)
    end = float(args.endbeta)

    num_coeff = int(args.num_coeff)
    block_size = int(args.block_size)
    training_size = int(args.training_size)
    tone = int(args.tone)

    weight_type_of_stress = args.stress_or_unstress

    print args

    data_dict = {
        250 : 'e',
        450 : 'i',
        950 : 't'
    }

    syllable_predicted_dct_path = '/work/w21/decha/Interspeech_2017/Speech_synthesis/Syllable_level/C_all_coeff/testrun/out_all/tsc/a-{}/infer/a-{}/demo/seed-00/M-{}/B-{}/num_iters-5/dur/predictive_distribution/'.format(data_dict[training_size], data_dict[training_size], block_size, block_size)

    if training_size == 250:
        base_frame_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/Experiment_A/01_manual_stress_labeling/testrun/out/tsc/a-e/infer/a-e/demo/seed-00/M-1024/B-1024/num_iters-5/'
    elif training_size == 450:
        base_frame_path = '/work/w21/decha/Interspeech_2017/GPR_data/450_with_stress_manual/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/'

    mask = 'gen'

    method = '/Script_26/Exp_1_no_zeroth/Syllable_training_size_{}/block_size_{}/num_coeff_{}/tone_{}/'.format(training_size, block_size, num_coeff, tone)

    outname = '/work/w21/decha/Interspeech_2017/Result/{}/'.format(method)

    original_path = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'

    koriyama_gen_path = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/'

    syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

    phone_in_syllable_object_path = '/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/j/'

    frame_predicted_lf0_path = '{}/lf0/predictive_distribution/'.format(base_frame_path)
    vuv_predicted_path = '{}/vuv/predictive_distribution/'.format(base_frame_path)

    stress_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'

    basename = 'tscsdj'

    for b in np.arange(start, end, increment):

        beta = b

        print strftime("%Y-%m-%d %H:%M:%S", gmtime())

        print 'Alpha : Beta : ', b, alpha

        outbase = outname
        outpath = '{}/Alpha_{}_Beta_{}/lf0/'.format(outbase, alpha, beta)
        figure_path = '{}/Alpha_{}_Beta_{}/fig/'.format(outbase, alpha, beta)

        Utility.make_directory(outpath)
        Utility.make_directory(figure_path)

        for num in range(1, 51):

            name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    

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
                'original_vuv': original_vuv,
                'num_coeff': num_coeff
            }

            cal_lf0(config)

        # Start for distortion

        UNDEF_VALUE = -1.0e+10

        stress_list = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'
        mono_label = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

        org_for_distortion = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'
        syn_for_distortion = outpath

        lf0_distortion_syn_is_gpr_format(org_for_distortion, syn_for_distortion, stress_list, mono_label)

    pass
