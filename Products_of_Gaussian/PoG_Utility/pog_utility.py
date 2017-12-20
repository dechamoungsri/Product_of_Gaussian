
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import re

from numpy.linalg import inv

import math

class PoGUtility(object):

    @staticmethod
    def generate_DCT_W_without_consonant_on_unstress_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone):
        all_w = PoGUtility.gen_W_without_consonant_on_unstress_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def gen_W_without_consonant_on_unstress_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s, st) in enumerate(zip(dur_list, p_in_s_file, stress)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            cur_vuv = vuv[offset_x+consonant:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if ( ((consonant+tail+head) > d ) | ( (st[0] =='1')) | (not ( st[1] == '{}'.format(tone) )) ):
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant - tail - head
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if head != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                if tail != 0:
                    local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W_without_consonant_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone):
        all_w = PoGUtility.gen_W_without_consonant_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def gen_W_without_consonant_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s, st) in enumerate(zip(dur_list, p_in_s_file, stress)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            cur_vuv = vuv[offset_x+consonant:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if ( ((consonant+tail+head) > d ) | (not ( st[1] == '{}'.format(tone) )) ):
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant - tail - head
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if head != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                if tail != 0:
                    local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W_without_consonant_on_stress_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone):
        all_w = PoGUtility.gen_W_without_consonant_on_stress_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def gen_W_without_consonant_on_stress_vuv_head_tail_tone(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv, tone):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s, st) in enumerate(zip(dur_list, p_in_s_file, stress)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            cur_vuv = vuv[offset_x+consonant:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if ( ((consonant+tail+head) > d ) | (not (st[0] =='1')) | (not ( st[1] == '{}'.format(tone) )) ):
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant - tail - head
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if head != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                if tail != 0:
                    local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w


    @staticmethod
    def generate_DCT_W_without_consonant_on_stress_vuv_head_tail(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv):
        all_w = PoGUtility.gen_W_without_consonant_on_stress_vuv_head_tail(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def gen_W_without_consonant_on_stress_vuv_head_tail(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s, st) in enumerate(zip(dur_list, p_in_s_file, stress)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            cur_vuv = vuv[offset_x+consonant:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if ((consonant+tail+head) > d )| (not (st[0] =='1') ):
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant - tail - head
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if head != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                if tail != 0:
                    local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W_without_consonant_on_stress_vuv(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv):
        all_w = PoGUtility.gen_W_without_consonant_on_stress_vuv(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def gen_W_without_consonant_on_stress_vuv(number_of_frame, dur_list, num_coeff, p_in_s_file, stress, vuv):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s, st) in enumerate(zip(dur_list, p_in_s_file, stress)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            cur_vuv = vuv[offset_x+consonant:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if ((consonant+tail) > d )| (not (st[0] =='1') ):
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant - tail
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if tail != 0:
                    local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W_without_consonant_on_stress(number_of_frame, dur_list, num_coeff, p_in_s_file, stress):
        all_w = PoGUtility.gen_W_without_consonant_on_stress(number_of_frame, dur_list, num_coeff, p_in_s_file, stress)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def gen_W_without_consonant_on_stress(number_of_frame, dur_list, num_coeff, p_in_s_file, stress):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s, st) in enumerate(zip(dur_list, p_in_s_file, stress)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            if ((consonant) > d )| (not (st =='1') ):

                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W_without_consonant(number_of_frame, dur_list, num_coeff, p_in_s_file):
        all_w = PoGUtility.gen_W_without_consonant(number_of_frame, dur_list, num_coeff, p_in_s_file)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w

    @staticmethod
    def gen_W_without_consonant(number_of_frame, dur_list, num_coeff, p_in_s_file):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s) in enumerate(zip(dur_list, p_in_s_file)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            if (consonant) > d:
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - consonant
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w


    @staticmethod
    def gen_W_with_vuv_without_consonant(number_of_frame, dur_list, num_coeff, vuv, p_in_s_file):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        # for idx, d in enumerate(dur_list):
        for idx, (d, p_in_s) in enumerate(zip(dur_list, p_in_s_file)):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            if len(p_in_s) == 0:
                consonant = 0
            else:
                consonant = int(float(p_in_s[0])/float(50000.0))

            cur_vuv = vuv[offset_x+consonant:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if (head+tail+consonant) > d:
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - (head+tail) - consonant
                local_w = PoGUtility.generate_W_for_DCT(voice_frame, num_coeff)
                if head != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, head), dtype='float'), local_w) , axis = 1)
                if tail != 0:
                    local_w = np.concatenate( ( local_w, np.zeros((num_coeff, tail), dtype='float') ) , axis = 1)
                if consonant != 0:
                    local_w = np.concatenate( ( np.zeros((num_coeff, consonant), dtype='float'), local_w) , axis = 1)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
    def generate_DCT_W_with_vuv_without_consonant(number_of_frame, dur_list, num_coeff, vuv, p_in_s_file):
        all_w = PoGUtility.gen_W_with_vuv_without_consonant(number_of_frame, dur_list, num_coeff, vuv, p_in_s_file)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w


    @staticmethod
    def find_head_and_tail(vuv_list):
        head_count = 0
        for v in vuv_list:
            if v==-1: 
                head_count+=1
            else:
                break

        tail_count = 0
        for v in reversed(vuv_list):
            if v==-1: 
                tail_count+=1
            else:
                break

        return (head_count, tail_count)

    @staticmethod
    def gen_W_with_vuv(number_of_frame, dur_list, num_coeff, vuv):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        for idx, d in enumerate(dur_list):

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            cur_vuv = vuv[offset_x:offset_x+d]
            head, tail = PoGUtility.find_head_and_tail(cur_vuv)

            if (head+tail) > d:
                local_w = np.zeros((num_coeff, d))
            else:
                voice_frame = d - (head+tail)
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
    def generate_DCT_W_with_vuv(number_of_frame, dur_list, num_coeff, vuv):
        all_w = PoGUtility.gen_W_with_vuv(number_of_frame, dur_list, num_coeff, vuv)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w

    @staticmethod
    def generate_DCT_W(number_of_frame, dur_list, num_coeff):
        all_w = PoGUtility.gen_W(number_of_frame, dur_list, num_coeff)

        w = [ ]

        for i in range(num_coeff):
            w.append([])

        for i in range( len(dur_list) ):
            for a in range(num_coeff):
                w[a].append(all_w[ num_coeff*i + a ])

        w = np.array(w)
        return w

    @staticmethod
    def gen_W(number_of_frame, dur_list, num_coeff):

        w = np.zeros( (num_coeff*len(dur_list), number_of_frame) )

        offset_x = 0
        offset_y = 0

        for idx, d in enumerate(dur_list):

            # print d

            if idx == (len(dur_list)-1):
                d = number_of_frame-offset_x

            local_w = PoGUtility.generate_W_for_DCT(d, num_coeff)

            for i in range(num_coeff):
                w[offset_y+i][offset_x:offset_x+d] = local_w[i]

            offset_x = offset_x + d
            offset_y = offset_y + num_coeff

        return w

    @staticmethod
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

    @staticmethod
    def gen_dur_and_name_list_for_phone(syllable_label_path, name, phone_duration_path):

        pattern = re.compile(r""".+/A:.+/D:.+\-(?P<num_phone>.+)\+.+/E:.+""",re.VERBOSE)

        dur_list = []
        for idx, line in enumerate(Utility.read_file_line_by_line(phone_duration_path)):
            spl = Utility.trim(line).split(' ')

            frame = int(spl[1]) - int(spl[0])
            frame = frame/50000

            dur_list.append(frame)

        names = []
        for idx, line in enumerate(Utility.read_file_line_by_line(syllable_label_path)):
            spl = Utility.trim(line).split(' ')

            match = re.match(pattern, line)
            if match:
                num_phone = match.group('num_phone')
                if num_phone == 'x':
                    num_phone = 1
                else:
                    num_phone = int(num_phone)

            for phone_index in xrange(num_phone):
                names.append('{}_{}_{}'.format(name, (idx+1), phone_index ))

        return (dur_list, names)

    @staticmethod
    def cal_sum_of_weight_part(v, w, cov):

        if not ( (len(v) == len(w)) ):
            raise Exception('Length of inputs unequal : v={} w={} '.format( len(v), len(w) ))

        s = []

        for i in range(len(v)):
            k = v[i] * np.dot(
                    np.transpose(w[i]), np.dot(
                        inv(cov), w[i]
                        )
                    )

            if i == 0:
                s = k
            else:
                s = s + k

        return s

    @staticmethod
    def cal_sum_of_mean_part(v, w, cov, mean):

        if not ( (len(v) == len(w)) & (len(w) == len(mean)) & (len(mean) == len(v)) ):
            raise Exception('Length of inputs unequal : v={} w={} mean={}'.format(len(v), len(w), len(mean)))

        s = []

        for i in range(len(v)):

            k = v[i] * np.dot(
                    np.transpose(w[i]), np.dot(
                        inv(cov), mean[i]
                        )
                    )

            if i == 0:
                s = k
            else:
                s = s + k

        return s

    @staticmethod
    def make_static_window_matrix(valid_frame_size, mask):

        W = np.eye(valid_frame_size, dtype='float32')

        # print (numpy.linalg.matrix_rank(W))

        return W.T

    @staticmethod
    def make_delta_window_matrix(valid_frame_size, mask):

        # (succeeding - current) * 0.5 + (current - preceding) * 0.5

        W = np.zeros((valid_frame_size, valid_frame_size), dtype='float32')

        j = 0
        for i in range(len(mask)):
            if mask[i] == False:
                continue

            if i > 0 and mask[i - 1]:
                W[j, j - 1] += -0.5
                W[j, j]     += 0.5
            if i < len(mask) - 1 and mask[i + 1]:
                W[j, j + 1] += 0.5
                W[j, j]     += -0.5

            j += 1

        return W

    @staticmethod
    def make_delta_delta_window_matrix(valid_frame_size, mask):

        # (succeeding - current) - (current - preceding)

        W = np.zeros((valid_frame_size, valid_frame_size), dtype='float32')

        j = 0
        for i in range(len(mask)):
            if mask[i] == False:
                continue

            if i > 0 and mask[i - 1]:
                W[j, j - 1] += 1.0
                W[j, j]     += -1.0
            if i < len(mask) - 1 and mask[i + 1]:
                W[j, j + 1] += 1.0
                W[j, j]     += -1.0

            j += 1

        return W

    @staticmethod
    def generate_W_for_GPR_generate_features(number_of_sample, vuv_list):

        # all_w = PoGUtility.generate_W_for_dynamic_feature_extraction(number_of_sample)

        # w = [ [], [], [] ]
        # for i in range(number_of_sample):
        #     for a in range(3):
        #         w[a].append(all_w[ 3*i + a ])

        # print len(vuv_list), number_of_sample

        mask = np.ones(len(vuv_list), dtype=bool)
        mask[vuv_list==-1] = False

        w = [
            PoGUtility.make_static_window_matrix(number_of_sample, mask),
            PoGUtility.make_delta_window_matrix(number_of_sample, mask),
            PoGUtility.make_delta_delta_window_matrix(number_of_sample, mask)
        ]

        w = np.array(w)
        return w

    @staticmethod
    def generate_W_for_dynamic_feature_extraction(number_of_sample):

        dy_dim = 3
        first_degree_dynamic = np.array([-1.0/2, 0, 1.0/2])
        second_degree_dynamic = np.array([1, -2, 1])

        w_matrix = np.zeros((number_of_sample*dy_dim, number_of_sample))

        for n in range(number_of_sample):

            if not (n==0):
                w_matrix[n*dy_dim+0][n-1] = 0
                w_matrix[n*dy_dim+1][n-1] = first_degree_dynamic[0]
                w_matrix[n*dy_dim+2][n-1] = second_degree_dynamic[0]

            w_matrix[n*dy_dim+0][n] = 1
            w_matrix[n*dy_dim+1][n] = first_degree_dynamic[1]
            w_matrix[n*dy_dim+2][n] = second_degree_dynamic[1]

            if not ( n==(number_of_sample-1) ):
                w_matrix[n*dy_dim+0][n+1] = 0
                w_matrix[n*dy_dim+1][n+1] = first_degree_dynamic[2]
                w_matrix[n*dy_dim+2][n+1] = second_degree_dynamic[2]

        return w_matrix

        pass

    @staticmethod
    def generate_DCT(data, number_of_dct):

        out = []

        for i in range(number_of_dct):
            o = 0
            for n in range( len(data) ):
                o = o + (2.0/len(data) * data[n] * math.cos( math.pi / len(data) * i * (n+0.5) ))

            out.append(o)

        return out

        pass

    @staticmethod
    def generate_inverse_DCT(DCT_coeff, number_of_data, start=0):

        out = []

        for i in range(number_of_data):
            o = 0.5 * DCT_coeff[0] 
            for n in range(start, len(DCT_coeff)-1):

                nn = n+1

                o = o + (DCT_coeff[nn] * math.cos( math.pi / number_of_data * nn * (i+0.5) ) )

            out.append(o)

        return out

        pass

    @staticmethod
    def generate_W_for_DCT(number_of_sample, number_of_coeff):
        K = float(number_of_coeff)
        N = float(number_of_sample)

        w_matrix = np.zeros((number_of_coeff, number_of_sample))

        for k in range(number_of_coeff):
            for n in range(number_of_sample):

                w = (2.0/N) * math.cos( 
                        math.pi / N * k * ( n + 0.5 ) 
                )

                w_matrix[k][n] = w

        return w_matrix
        

    @staticmethod
    def read_file_to_W(label_file):

        pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+/A:.+/D:.+\-(?P<phone_num>.+)\+.+/E:.+""",re.VERBOSE)

        phone_list = []

        for line in Utility.read_file_line_by_line(label_file):
            # print line
            match = re.match(pattern, line)
            if match:
                phone_num = match.group('phone_num')
                # print phone_num
                if phone_num == 'x' : 
                    phone_list.append(1)
                else:
                    phone_list.append(int(phone_num))

        row = len(phone_list)
        column = sum(phone_list)

        # print row, column

        w = []

        cur = 0

        for i in phone_list:
            r = np.zeros(column)
            r[cur:cur+i] = 1
            w.append(r)
            cur = cur+i

        w = np.array(w)
        # print w

        # for idx, i in enumerate(phone_list):
        #     print i, w[idx]

        return w
        pass

    @staticmethod
    def read_mean_and_cov_of_predictive_distribution(predictive_dist_path):
        mean_path = '{}/mean.npy'.format(predictive_dist_path)
        cov_path = '{}/cov.npy'.format(predictive_dist_path)

        mean = np.load(mean_path)
        cov = np.load(cov_path)

        # print mean
        # print cov

        return (mean, cov)

    @staticmethod
    def cal_invert_P(W, cov):
        P_inv = np.dot( 
                np.dot( np.transpose(W) , inv(cov) ) 
                , W )
        return P_inv

    @staticmethod
    def cal_R(W, cov, mean):
        r = np.dot( 
                np.dot( np.transpose(W) , inv(cov) ) 
                , mean )
        return r

    @staticmethod
    def cal_product_of_gaussian(R1, inv_P1, R2, inv_P2, alpha=1.0, beta=1.0):

        cov_inv = alpha * inv_P1 + beta * inv_P2
        cov = inv(cov_inv)

        mean = np.dot(cov, 
            ( 
                (alpha * R1) + (beta * R2) 
                ) 
            )

        return mean, cov

        pass

    @staticmethod
    def cal_mean_variance_of_product_of_gaussian(W, syl_mean, syl_cov, ph_mean, ph_cov, alpha=1, beta=1):

        P_inv = np.dot( 
                np.dot( np.transpose(W) , inv(syl_cov) ) 
                , W )
            
        r = np.dot( 
                np.dot( np.transpose(W) , inv(syl_cov) ) 
                , syl_mean )

        cov_inv = beta * P_inv + alpha * inv(ph_cov)
        cov = inv(cov_inv)

        mean = np.dot(cov, ( (beta * r) + (alpha * np.dot( inv(ph_cov), ph_mean )) ) )

        # print mean, cov

        return (mean, cov)

        pass

    """docstring for PoGUtility"""
    def __init__(self, arg):
        super(PoGUtility, self).__init__()
        
