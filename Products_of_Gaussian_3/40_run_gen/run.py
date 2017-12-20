
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../../Products_of_Gaussian/')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility
from PoG_Utility.plot_utility import PlotUtility
from joint_module import JointModule

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct
from numpy.linalg import inv

from sklearn.metrics.pairwise import rbf_kernel

from scipy import array, linalg, dot

import os
import sklearn, sklearn.metrics

import numpy

import itertools

import argparse

from time import gmtime, strftime

import datetime

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

            if not (st[0] == '1'):
                st[0] = '0'

            if (st[0] == str(stress_type)) & ( st[1] == '{}'.format(tone) ):
                stress_index = np.append(stress_index, np.arange(start, end), axis=0 )

        # print stress_index

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
    print('Only specific case LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_stress_list)))

    return rmse

    pass

def lf0_gen_with_vuv(lf0, vuv_list):
    unvoice = np.where(vuv_list==-1)[0]
    lf0[unvoice] = unvoice_value

    return lf0

def cal_lf0(config):

    base_path = config['base_path']
    label_path = config['label_path']
    name = config['name']
    # outfilepath = config['outfilepath']
    var_path = config['var_path']
    syllable_base_path = config['syllable_base_path']
    syllable_var_path = config['syllable_var_path']
    original = config['original']
    koriyama_gen = config['koriyama_gen']
    # figure_path = config['figure_path']
    ph_in_syl_object_path = config['phone_in_syllable_object_path']
    stress_type = config['stress_type']
    original_vuv = config['original_vuv']
    zero_base_path = config['zero_base_path']
    zero_var_path = config['zero_var_path']

    p_in_s_file = Utility.load_obj(ph_in_syl_object_path)

    vuv = np.load('{}/class.npy'.format(config['vuv_path']))

    A_list = []
    B_list = []

    #--------Frame-------#

    lf0_mean = np.load('{}/mean.npy'.format(base_path))
    lf0_cov = np.load('{}/cov.npy'.format(base_path))
    number_of_frame = len(lf0_cov)

    frame_A, frame_B = JointModule.cal_for_frame_level(var_path, vuv, lf0_cov, lf0_mean, alpha)
    A_list.append(frame_A)
    B_list.append(frame_B)

    L = linalg.cholesky(frame_A, lower=True)
    lf0 = linalg.cho_solve((L, True) , frame_B)

    frame_lf0_nomask = np.copy(lf0) 

    lf0[lf0<1] = np.nan

    frame_lf0 = np.copy(lf0) 

    #----------Phone level------------#

    config['phone_level_config']['number_of_frame'] = number_of_frame
    ph_A_1toN, ph_B_1toN = JointModule.cal_suprasegmental('phone', config['phone_level_config'],  coeff_end_position=num_coeff, coeff_start_position=1, use_consonant=False)
    A_list.append(ph_A_1toN)
    B_list.append(ph_B_1toN)

    #----------Phone level 0-th coeff------------#

    config['phone_level_zero_config']['number_of_frame'] = number_of_frame
    ph_A_0, ph_B_0 = JointModule.cal_suprasegmental('phone', config['phone_level_zero_config'],  coeff_end_position=1, use_consonant=False)
    A_list.append(ph_A_0)
    B_list.append(ph_B_0)

    #----------Syllable level------------#

    config['syllable_level_config']['number_of_frame'] = number_of_frame
    syl_A_1toN, syl_B_1toN = JointModule.cal_suprasegmental('syllable', config['syllable_level_config'],  coeff_end_position=num_coeff, coeff_start_position=1, use_consonant=True)
    A_list.append(syl_A_1toN)
    B_list.append(syl_B_1toN)

    #----------Syllable level 0-coeff--------#

    config['syllable_level_zero_config']['number_of_frame'] = number_of_frame
    syl_A_0, syl_B_0 = JointModule.cal_suprasegmental('syllable', config['syllable_level_zero_config'],  coeff_end_position=1, use_consonant=True)
    A_list.append(syl_A_0)
    B_list.append(syl_B_0)

    #----------Combine Model--------#

    return (A_list, B_list)

    # a_sum = np.zeros(frame_A.shape, dtype=np.float)
    # for a in A_list:
    #     a_sum = a_sum + a

    # b_sum = np.zeros(frame_B.shape, dtype=np.float)
    # for b in B_list:
    #     b_sum = b_sum + b

    # L = linalg.cholesky(a_sum, lower=True)
    # lf0 = linalg.cho_solve((L, True) , b_sum)

    # # print lf0.shape

    # lf0[lf0<1] = np.nan

    # if args.plot:
    #     PlotUtility.plot([original, frame_lf0_nomask, lf0], ['original', 'Single', 'Multi+0'], '{}/{}_no_mask.eps'.format(figure_path, name))

    # lf0 = lf0_gen_with_vuv(lf0, vuv)
    # lf0[lf0<1] = np.nan

    # frame_lf0 = lf0_gen_with_vuv(frame_lf0, vuv)
    # frame_lf0[frame_lf0<1] = np.nan
    
    # np.save(outfilepath, lf0)

    # if args.plot:
    #     PlotUtility.plot([original, frame_lf0, lf0], ['original', 'Single', 'Multi+0'], '{}/{}_multi.eps'.format(figure_path, name))

    pass

if __name__ == '__main__':

    unvoice_value = -1.00000000e+10

    alpha = 1.0
    beta = 1.0

    increment = 0.2

    parser = argparse.ArgumentParser()

    parser.add_argument('-method_name')
    parser.add_argument('-mainoutpath')

    parser.add_argument('-start_ph_0')
    parser.add_argument('-end_ph_0')

    parser.add_argument('-start_ph_1toN')
    parser.add_argument('-end_ph_1toN')

    parser.add_argument('-start_syl_1toN')
    parser.add_argument('-end_syl_1toN')

    parser.add_argument('-start_syl_0')
    parser.add_argument('-end_syl_0')

    parser.add_argument('-plot', action='store_true')
    parser.add_argument('-training_size')
    parser.add_argument('-tone', required=True)
    parser.add_argument('-stress_type', required=True)
    parser.add_argument('-tone_folder', required=True)
    args = parser.parse_args()

    start_ph_0 = float(args.start_ph_0)
    end_ph_0 = float(args.end_ph_0)

    start_ph_1toN = float(args.start_ph_1toN)
    end_ph_1toN = float(args.end_ph_1toN)

    start_syl_1toN = float(args.start_syl_1toN)
    end_syl_1toN = float(args.end_syl_1toN)

    start_syl_0 = float(args.start_syl_0)
    end_syl_0 = float(args.end_syl_0)

    method_name = args.method_name
    mainoutpath = args.mainoutpath

    num_coeff = 3
    block_size = 256
    training_size = int(args.training_size)
    tone = int(args.tone)
    tone_folder = str(args.tone_folder)
    stress_type = str(args.stress_type)

    print args

    # optimization
    optimal_list = itertools.product(

        [1.0],

        np.arange(start_ph_1toN, end_ph_1toN, increment),
        
        np.arange(start_syl_1toN, end_syl_1toN, increment), 
        np.arange(start_syl_0, end_syl_0, increment)
    )

    ph0_optimal = np.arange(start_ph_0, end_ph_0, increment)

    data_dict = {
        250 : 'e',
        450 : 'i',
        950 : 't'
    }

    now = datetime.datetime.now()

    method = '/{}_{}/Syllable_training_size_{}_block_size_{}_num_coeff_{}/tone_{}/'.format(method_name, now.strftime("%Y-%m-%d"), training_size, block_size, num_coeff, tone)

    outname = '{}/{}/'.format(mainoutpath, method)

    non_optimal_path = '{}/raw_calculation/'.format(outname)
    Utility.make_directory(non_optimal_path)

    #------------ General info--------------#

    original_path = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'

    koriyama_gen_path = '/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/'

    # syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'
    syl_duration_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time_syllable_remove_silence/tsc/sd/j/'
    ph_duration_path = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/j/'

    phone_in_syllable_object_path = '/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/j/'

    stress_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'

    basename = 'tscsdj'

    #----------frame-level path------------#

    if training_size == 250:
        base_frame_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/Experiment_A/01_manual_stress_labeling/testrun/out/tsc/a-e/infer/a-e/demo/seed-00/M-1024/B-1024/num_iters-5/'
    elif training_size == 450:
        base_frame_path = '/work/w21/decha/Interspeech_2017/GPR_data/450_with_stress_manual/infer/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/'
    frame_predicted_lf0_path = '{}/lf0/predictive_distribution/'.format(base_frame_path)
    vuv_predicted_path = '{}/vuv/predictive_distribution/'.format(base_frame_path)

    #----------phone-level path------------#
    if stress_type == '0':
        phone_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis_2/Phone_level/GPR-Run-unstress/B_other_coeff/testrun/'
        phone_zero_coeff_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis_2/Phone_level/GPR-Run-unstress/A_zeroth_coeff/testrun'
    else:
        phone_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis_2/Phone_level/GPR-Run-stress/B_other_coeff/testrun/'
        phone_zero_coeff_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis_2/Phone_level/GPR-Run-stress/A_zeroth_coeff/testrun'

    phone_predicted_dct_path = '{}/out_{}/tsc/a-{}/infer/a-{}/demo/seed-00/M-{}/B-{}/num_iters-5/dur/predictive_distribution/'.format(phone_predicted_basepath, tone_folder, data_dict[training_size], data_dict[training_size], block_size, block_size)

    phone_zero_coeff_predicted_dct_path = '{}/out_{}/tsc/a-{}/infer/a-{}/demo/seed-00/M-{}/B-{}/num_iters-5/dur/predictive_distribution/'.format(phone_zero_coeff_predicted_basepath, tone_folder, data_dict[training_size], data_dict[training_size], block_size, block_size)

    #----------syllable-level path------------#
    if stress_type == '0':
        syllable_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis/Syllable_level/B_other_coeff/testrun/'
        zero_coeff_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis/Syllable_level/A_zeroth_coeff/testrun/'
    else:
        syllable_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis/05_syllable_level_3_dct_no_zeroth/testrun/'
        zero_coeff_predicted_basepath = '/work/w21/decha/Interspeech_2017/Speech_synthesis/06_zeroth_coeff_run_tree_05/testrun/'

    syllable_predicted_dct_path = '{}/out_{}/tsc/a-{}/infer/a-{}/demo/seed-00/M-{}/B-{}/num_iters-5/dur/predictive_distribution/'.format(syllable_predicted_basepath, tone_folder, data_dict[training_size], data_dict[training_size], block_size, block_size)

    zero_coeff_predicted_dct_path = '{}/out_{}/tsc/a-{}/infer/a-{}/demo/seed-00/M-{}/B-{}/num_iters-5/dur/predictive_distribution/'.format(zero_coeff_predicted_basepath, tone_folder, data_dict[training_size], data_dict[training_size], block_size, block_size)

    #----------Running------------#

    main_out_data = dict()
    for num in range(1, 51):

        name = '{}{}'.format(basename, Utility.fill_zero(num, 2))    

        # outfile = '{}/{}.npy'.format(outpath, name)

        base_path = '{}/{}/'.format( frame_predicted_lf0_path, name )
        label_path = '{}/{}.lab'.format( syl_duration_path, name )

        phone_label_path = '{}/{}.lab'.format( ph_duration_path, name )

        var_path = '{}/inv_dimension_cov.npy'.format(frame_predicted_lf0_path)

        #--------Phone--------#

        phone_base_path = '{}/{}/'.format( phone_predicted_dct_path, name )
        phone_var_path =  '{}/inv_dimension_cov.npy'.format( phone_predicted_dct_path )

        phone_zero_base_path = '{}/{}/'.format( phone_zero_coeff_predicted_dct_path, name )
        phone_zero_var_path =  '{}/inv_dimension_cov.npy'.format( phone_zero_coeff_predicted_dct_path )

        #--------Syllable--------#

        syllable_base_path = '{}/{}/'.format( syllable_predicted_dct_path, name )
        syllable_var_path =  '{}/inv_dimension_cov.npy'.format( syllable_predicted_dct_path )

        zero_base_path = '{}/{}/'.format( zero_coeff_predicted_dct_path, name )
        zero_var_path =  '{}/inv_dimension_cov.npy'.format( zero_coeff_predicted_dct_path )

        vuv_path = '{}/{}/'.format( vuv_predicted_path, name )

        original = Utility.read_lf0_into_ascii('{}/{}.lf0'.format(original_path, name))
        original = np.array(original)

        original_vuv = np.copy(original)
        original_vuv[original_vuv<0] = -1
        original_vuv[original_vuv>=0] = +1

        original[original<0] = np.nan

        koriyama_gen = np.load('{}/{}.npy'.format(koriyama_gen_path, name))
        koriyama_gen[koriyama_gen<0] = np.nan

        stress_list = '{}/{}.npy'.format(stress_path, name)
        stress_list = np.load(stress_list)

        config = {
            'base_path' : base_path,
            'label_path' : label_path,
            'name' : name,
            # 'outfilepath' : outfile,
            'var_path' : var_path, 

            #------ Phone -----#
            'phone_base_path': phone_base_path,
            'phone_var_path' : phone_var_path,

            'phone_zero_base_path': phone_zero_base_path,
            'phone_zero_var_path': phone_zero_var_path,

            #------ Syllable -----#
            'syllable_base_path': syllable_base_path,
            'syllable_var_path' : syllable_var_path,

            'zero_base_path': zero_base_path,
            'zero_var_path': zero_var_path,
            
            'vuv_path' : vuv_path,
            'original' : original,
            'koriyama_gen' : koriyama_gen,
            # 'figure_path' : figure_path,
            'phone_in_syllable_object_path': '{}/{}.dur'.format(phone_in_syllable_object_path, name),
            'stress_list': stress_list,
            'original_vuv': original_vuv,
            'tone': tone,
            'stress_type': stress_type
        }

        phone_level_config = {
            'label_path': config['label_path'],

            'ph_duration_path': phone_label_path,

            'name': config['name'],
            'original': config['original'],

            'base_path': config['phone_base_path'],
            'var_path': config['phone_var_path'],

            'num_coeff': num_coeff,
            'stress_list': config['stress_list'], 
            'vuv_path': config['vuv_path'],
            'tone': config['tone'],
            'stress_type': config['stress_type'],
            'phone_in_syllable_object_path': config['phone_in_syllable_object_path']
        }

        phone_level_zero_config = {
            'label_path': config['label_path'],

            'ph_duration_path': phone_label_path,
            
            'name': config['name'],
            'original': config['original'],

            'base_path': config['phone_zero_base_path'],
            'var_path': config['phone_zero_var_path'],

            'num_coeff': num_coeff,
            'stress_list': config['stress_list'], 
            'vuv_path': config['vuv_path'],
            'tone': config['tone'],
            'stress_type': config['stress_type'],
            'phone_in_syllable_object_path': config['phone_in_syllable_object_path']
        }

        syllable_level_config = {
            'label_path': config['label_path'],
            'name': config['name'],
            'original': config['original'],

            'base_path': config['syllable_base_path'],
            'var_path': config['syllable_var_path'],

            'num_coeff': num_coeff,
            'stress_list': config['stress_list'], 
            'vuv_path': config['vuv_path'],
            'tone': config['tone'],
            'stress_type': config['stress_type'],
            'phone_in_syllable_object_path': config['phone_in_syllable_object_path']
        }

        syllable_level_zero_config = {
            'label_path': config['label_path'],
            'name': config['name'],
            'original': config['original'],

            'base_path': config['zero_base_path'],
            'var_path': config['zero_var_path'],

            'num_coeff': num_coeff,
            'stress_list': config['stress_list'], 
            'vuv_path': config['vuv_path'],
            'tone': config['tone'],
            'stress_type': config['stress_type'],
            'phone_in_syllable_object_path': config['phone_in_syllable_object_path']
        }

        config['phone_level_config'] = phone_level_config
        config['phone_level_zero_config'] = phone_level_zero_config

        config['syllable_level_config'] = syllable_level_config
        config['syllable_level_zero_config'] = syllable_level_zero_config

        vuv = np.load('{}/class.npy'.format(config['vuv_path']))
        A_list, B_list = cal_lf0(config)
        main_out_data[name] = (A_list, B_list, vuv)
        Utility.save_obj(main_out_data[name], '{}/{}.pkl'.format(non_optimal_path, name))

    for opt in optimal_list:
        old_rmse = 1000000000
        for ph0 in ph0_optimal:

            print strftime("%Y-%m-%d %H:%M:%S", gmtime())

            print 'Alpha: const_ph_1toN: const_ph_0: const_syl_1toN: const_syl_0:'
            print opt[0], opt[1], ph0, opt[2], opt[3]

            outbase = outname
            outpath = '{}/Alpha_{}_const_ph_1toN_{}_const_ph_0_{}_const_syl_1toN_{}_const_syl_0_{}/lf0/'.format(outbase, opt[0], opt[1], ph0, opt[2], opt[3] )
            figure_path = '{}/Alpha_{}_const_ph_1toN_{}_const_ph_0_{}_const_syl_1toN_{}_const_syl_0_{}/fig/'.format(outbase, opt[0], opt[1], ph0, opt[2], opt[3])

            opt_used = [opt[0], opt[1], ph0, opt[2], opt[3]]
            
            Utility.make_directory(outpath)
            Utility.make_directory(figure_path)

            for n in main_out_data:

                A_list, B_list, vuv = main_out_data[n]
                a_sum = np.zeros(A_list[0].shape, dtype=np.float)
                b_sum = np.zeros(B_list[0].shape, dtype=np.float)

                for a, b, const in zip(A_list, B_list, opt_used):
                    a_sum = a_sum + (const * a)
                    b_sum = b_sum + (const * b)

                L = linalg.cholesky(a_sum, lower=True)
                lf0 = linalg.cho_solve((L, True) , b_sum)       
                lf0 = lf0_gen_with_vuv(lf0, vuv)

                outfile = '{}/{}.npy'.format(outpath, n)
                np.save(outfile, lf0)

            # Start for distortion
            UNDEF_VALUE = -1.0e+10

            stress_list = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/stress_list/j/'
            mono_label = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/mono_syllable_remove_silence/tsc/sd/j/'

            org_for_distortion = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/j/'
            syn_for_distortion = outpath

            rmse = lf0_distortion_syn_is_gpr_format(org_for_distortion, syn_for_distortion, stress_list, mono_label)

            if rmse < old_rmse:
                old_rmse = rmse
            else :
                break

    pass
