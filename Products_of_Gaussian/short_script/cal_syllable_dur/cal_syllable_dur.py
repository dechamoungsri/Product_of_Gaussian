
import sys
# import numpy 
import numpy as np
import re
import sklearn, sklearn.metrics
# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility

def _calc_duration_distortion(self):

    _logger.info("Calc Duration Distortion")

    dur_true_list = []
    dur_pred_list = []
    for base in self._inference_data_set.make_base_list():
        param_file = os.path.join(self._parameter_generation_dir, 'param_mean', '{}.npy'.format(base))
        duration_vector = numpy.load(param_file)

        frame_file = os.path.join(self._frame_sequence_dir, '{:}.frmseq.pkl'.format(base))
        frame_sequence = cPickle.load(open(frame_file, 'rb'))

        for frame, dur_pred in zip(frame_sequence.iter(), duration_vector):
            if frame.get_phone_context('current_phoneme') in ['sil', 'pau']:
                continue

            dur_true_list.append(1000 * frame.get_feature_vector('dur'))
            dur_pred_list.append(1000 * dur_pred)

    # numpy.savetxt('dur.npy.txt', numpy.c_[dur_true_list, dur_pred_list])

    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(dur_true_list, dur_pred_list))
    _logger.info('RMSE: {:f} in {} phones'.format(rmse, len(dur_true_list)))

    self._write_distortion_file(rmse)

def get_org_syllable_list(filename):

    dur_list = []
    num_phone_list = []

    for line in Utility.read_file_line_by_line(filename):
        pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+/D:.+\-(?P<num_phone>.+)\+.+/E:.+""",re.VERBOSE)
        match = re.match(pattern, line)
        if match:
           num_phone = match.group('num_phone')

           start = match.group('start')
           end = match.group('end')

           # print start, end, num_phone

           d = float(int(end) - int(start)) / 10000000
           # print d
           dur_list.append( d )
           num_phone_list.append(num_phone)

    return (dur_list, num_phone_list)

    pass
    

def get_dur_list(dur_path):

    dur = np.load(dur_path)
    # print dur

    return dur

    pass

def get_dir_list_HMM(dur_path):

    dur = []

    for d in Utility.read_file_line_by_line(dur_path):
        if 'state' in d: 
            continue

        pattern = re.compile(r""".+\sduration=(?P<frame>.+)\s\(frame\).+""",re.VERBOSE)
        match = re.match(pattern, d)
        if match:
           frame = match.group('frame')
           # print frame
           dur.append( [float(frame) * 50000 / 10000000] )

    return dur

    pass

def cal_syllable_dur(dur_path, syl_dur_path, hmm=False):

    org_all, gen_all = [], []

    file_count = 0

    # print Utility.list_file(dur_path)

    for dur_file in Utility.list_file(dur_path):
        # print dur_file
        if hmm : 
            if 'dur' not in dur_file:
                continue
        elif 'npy' not in dur_file:
            continue

        file_count = file_count + 1

        basename = Utility.get_basefilename(dur_file)
        # print basename

        org_path = '{}/{}.lab'.format(syl_dur_path, basename)

        org_dur_list, num_phone = get_org_syllable_list(org_path)

        if not hmm :
            gen_dur = get_dur_list('{}/{}'.format(dur_path, dur_file))
        else :
            gen_dur = get_dir_list_HMM('{}/{}'.format(dur_path, dur_file))

        gen_syn_dur = []

        idx = 0

        # print len(num_phone)

        # print num_phone

        # print gen_dur

        summ = 0

        for num in num_phone:

            # print num

            if num == 'x':
                gen_syn_dur.append(gen_dur[idx][0])
                idx = idx + 1
            else:
                syllable_duration = 0

                summ = summ + int(num)

                for n in range(1, int(num)+1 ) :
                    # print n, num
                    syllable_duration = syllable_duration + gen_dur[idx][0]
                    idx = idx + 1
                    # print syllable_duration
                gen_syn_dur.append(syllable_duration)

        # print len(num_phone), idx, len(gen_dur), summ

        if len(gen_syn_dur) != len(org_dur_list):
            print 'Not equal'
            print dur_path

        # print gen_syn_dur

        for idx, num in enumerate( num_phone ):
            if num == 'x':
                continue

            org = org_dur_list[idx] * 1000
            gen = gen_syn_dur[idx] * 1000

            org_all.append(org)
            gen_all.append(gen)

            # print org, gen

        # break

    # RMSE for dur in syllable
    rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(org_all, gen_all))

    # print file_count

    print rmse

    pass

def hmm_frame_to_mono_label(dur_path, mono_path, out_path):

    for dur_file in Utility.list_file(dur_path):
        
        if not 'dur' in dur_file: continue

        base = Utility.get_basefilename(dur_file)
        # print base

        dur = '{}/{}'.format(dur_path, dur_file)
        # print dur

        dur_list = get_dir_list_HMM(dur)
        # print dur_list

        mono = '{}/{}.lab'.format(mono_path, base)
        mono_list = load_mono(mono)

        out_file = '{}/{}.lab'.format(out_path, base)

        # print len(dur_list), len(mono_list)

        if len(dur_list) != len(mono_list):
            print base

        start = 0

        out = []

        for idx, d in enumerate(dur_list):
            # print dur_list[idx][0], mono_list[idx]
            
            o = '{}\t{}\t{}'.format( int(start), int(start+(dur_list[idx][0] * 10000000)), mono_list[idx])
            out.append(o)

            start = start+(dur_list[idx][0] * 10000000)

        Utility.write_to_file_line_by_line(out_file, out)

        # sys.exit()

    pass

def load_mono(mono_file):

    m = []

    for line in Utility.read_file_line_by_line(mono_file):
        spl = line.split(' ')

        ph = Utility.trim(spl[2])
        # print ph

        m.append(ph)

    # print m
    return m

    pass

def load_dur_file(num_phone, mono_list, outpath):

    dur_list = []

    idx = 0
    for num in num_phone:
        # print num
        if num == 'x':
            
            spl = mono_list[idx].split('\t')
            dur = int(spl[1]) - int(spl[0])

            syl_dur = [dur]

            dur_list.append(syl_dur)

            # print syl_dur

            idx = idx + 1
        else:

            syl_dur = []

            for n in range(1, int(num)+1 ) :
                # print n, num
                spl = mono_list[idx].split('\t')
                dur = int(spl[1]) - int(spl[0])

                syl_dur.append(dur)
                idx = idx + 1

            dur_list.append(syl_dur)
            # print syl_dur

    # print dur_list
    Utility.save_obj(dur_list, outpath)

    pass

############################################################
if __name__ == '__main__':
    syl_dur_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time_syllable_remove_silence/tsc/sd/j/'

    # path = '/work/w16/decha/decha_w16/spec_com_work_space/speech_param/450/01_GPR/'
    # path = '/work/w16/decha/decha_w16/spec_com_work_space/speech_param/450/02_GPR_with_multi_level/'
    # path = '/work/w16/decha/decha_w16/spec_com_work_space/speech_param/450/03_HMM/'
    path = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/03_PoG/'

    mono_path = '{}/mono_label/'.format(path)

    outpath = '{}/mono_to_syl_dur/'.format(path)
    Utility.make_directory(outpath)

    for syl in Utility.list_file(syl_dur_path):
        print syl
        syl_path = '{}/{}'.format(syl_dur_path, syl)
        dur_list, num_phone = get_org_syllable_list(syl_path)

        mono_file = '{}/{}'.format(mono_path, syl)
        mono_list = Utility.read_file_line_by_line(mono_file)

        out_file = '{}/{}'.format(outpath, syl)

        # print num_phone
        load_dur_file(num_phone, mono_list, out_file)

        # sys.exit()

############################################################
# if __name__ == '__main__':
#     # Gen mono for HMM

#     dur_path = '/work/w16/decha/decha_w16/spec_com_work_space/speech_param/450/03_HMM/parm/'

#     mono_path = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/j/'

#     out_path = '/work/w16/decha/decha_w16/spec_com_work_space/speech_param/450/03_HMM/mono_label/'

#     Utility.make_directory(out_path)

#     hmm_frame_to_mono_label(dur_path, mono_path, out_path)

############################################################
# if __name__ == '__main__':

#     syl_dur_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time_syllable_remove_silence/tsc/sd/j/'

#     for num in range(850, 950, 100):
#         # dur_path = '/work/w16/decha/decha_w16/spec_com_work_space/Speech_synthesis/09_HMM_FIX_DATA/out/straight/mht/{}/model/s5m1/gen/gv-0/parm/'.format(num)
#         dur_path = '/work/w15/decha/decha_w15/Specom_w15/09_HMM_Test_for_appropiate_set/09_850/out/straight/mht/{}/model/s5m1/gen/gv-0/parm/'.format(num)

#         cal_syllable_dur(dur_path, syl_dur_path, hmm=True)

############################################################

