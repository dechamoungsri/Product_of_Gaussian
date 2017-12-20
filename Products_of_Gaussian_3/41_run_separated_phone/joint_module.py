
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../../Products_of_Gaussian/')

from tool_box.util.utility import Utility
from PoG_Utility.pog_utility import PoGUtility

import numpy as np

class JointModule(object):
    """docstring for JointModule"""
    def __init__(self, arg):
        super(JointModule, self).__init__()
        self.arg = arg
    
    @staticmethod
    def gen_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=False, phone_part='no'):

        # print stress_list

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        for idx, (d, p_in_s, st, name) in enumerate(zip(dur_list, p_in_s_file, stress_list, names)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if use_consonant:
                if len(p_in_s) == 0:
                    consonant = 0
                else:
                    consonant = int(float(p_in_s[0])/float(50000.0))

                cur_vuv = vuv[offset_x:offset_x+d]
                head, tail = PoGUtility.find_head_and_tail(cur_vuv)

                if not (st[0] == '1'):
                    st[0] = '0'

                if ( ((consonant+tail+head) > d ) | (not (st[0] ==str(stress_type))) | (not ( st[1] == '{}'.format(tone) )) ):
                    local_w = np.zeros((num_coeff, d))
                else:
                    # print 'panda'
                    voice_frame = d - consonant - tail - head
                    local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                    if head != 0:
                        local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                    if tail != 0:
                        local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                    if consonant != 0:
                        local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            elif phone_part != 'no':
                cur_vuv = vuv[offset_x:offset_x+d]
                head, tail = PoGUtility.find_head_and_tail(cur_vuv)

                if not (st[0] == '1'):
                    st[0] = '0'

                if ( ((tail+head) > d ) | (not (st[0] == str(stress_type) )) | (not ( st[1] == '{}'.format(tone) )) | ( not (name.split('_')[2] == phone_part ) ) ):
                    local_w = np.zeros((num_coeff, d))
                else:
                    # print 'panda'
                    voice_frame = d - tail - head
                    local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                    if head != 0:
                        local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                    if tail != 0:
                        local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)

            else:
                cur_vuv = vuv[offset_x:offset_x+d]
                head, tail = PoGUtility.find_head_and_tail(cur_vuv)

                if not (st[0] == '1'):
                    st[0] = '0'

                if ( ((tail+head) > d ) | (not (st[0] == str(stress_type) )) | (not ( st[1] == '{}'.format(tone) )) ):
                    local_w = np.zeros((num_coeff, d))
                else:
                    # print 'panda'
                    voice_frame = d - tail - head
                    local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                    if head != 0:
                        local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                    if tail != 0:
                        local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=False, phone_part='no'):
        all_w = JointModule.gen_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=use_consonant, phone_part=phone_part)

        w = [ ]
        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w

    @staticmethod
    def cal_for_frame_level(var_path, vuv, lf0_cov, lf0_mean, alpha):

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

        return (frame_A, frame_B)

    @staticmethod
    def cal_suprasegmental(level, config, coeff_end_position, coeff_start_position=0, use_consonant=False, const=1.0, separated_phone='no'):

        syllable_label_path = config['label_path']
        name = config['name']
        original = config['original']
        base_path = config['base_path']
        var_path = config['var_path']
        number_of_frame = config['number_of_frame']
        num_coeff = config['num_coeff']
        stress_list = config['stress_list']
        vuv = np.load('{}/class.npy'.format(config['vuv_path']))
        tone = config['tone']
        stress_type = config['stress_type']

        ph_in_syl_object_path = config['phone_in_syllable_object_path']
        p_in_s_file = Utility.load_obj(ph_in_syl_object_path)

        if level == 'syllable':
            dur_list, names = PoGUtility.gen_dur_and_name_list(syllable_label_path, name)
        elif level == 'phone':
            dur_list, names = PoGUtility.gen_dur_and_name_list_for_phone(syllable_label_path, name, config['ph_duration_path'])
            
        if np.sum(dur_list) < len(original):
            dur_list[0] = dur_list[0] + len(original)-np.sum(dur_list)

        mean = np.load('{}/mean.npy'.format(base_path))
        cov = np.load('{}/cov.npy'.format(base_path))

        # Reshape var
        var = np.load('{}'.format(var_path))
        var = np.sum(var, axis=0)

        # Reshape mean
        temp_mean = []
        for i in range( len(mean[0]) ):
            temp_mean.append( mean[:,i] )
        mean = np.array(temp_mean)

        if separated_phone == 'no':
            w = JointModule.generate_DCT_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=use_consonant)
        elif separated_phone == 'vowel':
            w = JointModule.generate_DCT_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=use_consonant, phone_part='1')
        elif separated_phone == 'initial':
            w = JointModule.generate_DCT_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=use_consonant, phone_part='0')
        elif separated_phone == 'final':
            w = JointModule.generate_DCT_W(number_of_frame, dur_list, num_coeff, stress_list, vuv, tone, stress_type, p_in_s_file, names, use_consonant=use_consonant, phone_part='2')

        w = w[coeff_start_position:coeff_end_position]

        # s_B = const * PoGUtility.cal_sum_of_mean_part(var, w, cov, mean)
        # s_A = const * PoGUtility.cal_sum_of_weight_part(var, w, cov)
        s_B = PoGUtility.cal_sum_of_mean_part(var, w, cov, mean)
        s_A = PoGUtility.cal_sum_of_weight_part(var, w, cov)

        return (s_A, s_B)

