
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import matplotlib

font = {
        'size'   : 26}

matplotlib.rc('font', **font)

def data_size(dur_list):

    count = 0

    for d in dur_list:
        count = count + len(d)

    return count

def plot(org, hmm, gpr, gpr_with_multi_level, outfile):

    width = 0.2
    colors = ['r', 'b', 'g']
    org_list = Utility.load_obj(org)

    print org_list

    ind = np.arange( data_size(org_list) )

    plt.clf()
    fig = plt.gcf()
    size = fig.get_size_inches()
    print size
    fig.set_size_inches(len(ind) * 8 / 10/3/1.5  , 7/1.2)

    # f, ax = plt.subplots(3, sharex=True, sharey=True)

    for dur_idx, dur_path in enumerate( [hmm, gpr, gpr_with_multi_level] ): 

        plt.clf()

        data = Utility.load_obj(dur_path) 

        count = 0

        syllable_position = []

        phone_dur_list = []

        syl_dur_list = []

        for idx, d in enumerate( data ):

            phone_sum = 0
            ori_sum = 0

            for p_idx, p in enumerate( d ):
                # print p
                count = count + 1
                if len(d) == 1:
                    phone_dur_list.append(0)
                    phone_sum = phone_sum + 0
                    continue
                else :
                    phone_sum = phone_sum + p
                    ori_sum = ori_sum + org_list[idx][p_idx]

                    phone_dur_list.append( float(p - org_list[idx][p_idx])/50000 )

            syl_dur_list.append( float(phone_sum - ori_sum)/10000000 * 1000 )

            syllable_position.append(count)

        # print 'Length : ', len(phone_dur_list), len(ind)

        # ax[dur_idx].bar(ind, phone_dur_list,color=colors[dur_idx])

        ind = np.arange( len(syl_dur_list) )

        label = Utility.read_file_line_by_line('/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/syllable_time/j/tscsdj34.lab')

        l = []
        for lab in label:
            spl = lab.split(' ')
            l.append(spl[2])

        plt.bar(ind, syl_dur_list, color='0.5')
        plt.xticks(ind+0.5, l, rotation='-45')
        plt.yticks([-80, -40, 0, 40 , 80])

        # ax[dur_idx].set_xlim([2,20])
        # ax[dur_idx].set_ylim([-15,15])

        plt.xlim([1,21])
        plt.ylim([-80,100])

        # plt.xlabel('Syllables')
        plt.ylabel('Error [msec]')

        # for s in syllable_position:
        #     # print s
        #     ax[dur_idx].plot([s, s], ax[dur_idx].get_ylim(), 'k--', lw=0.5)
        titles = ['single', 'multi', 'pog']
        plt.tight_layout()
        plt.savefig('{}_{}_used.eps'.format( outfile, titles[dur_idx] ))
        

    pass

if __name__ == '__main__':

    org = '/work/w2/decha/Data/GPR_speccom_data/mono_to_syl_dur/'
    hmm = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/01_GPR/mono_to_syl_dur/'
    gpr = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/02_GPR_with_multi_level/mono_to_syl_dur/'
    gpr_with_multi_level = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/03_PoG/mono_to_syl_dur/'

    outpath = './dur_distortion_syl_specific/'
    Utility.make_directory(outpath)

    for lab in Utility.list_file(org):

        if '34' not in lab:
            continue

        print lab

        o = '{}/{}'.format(org, lab)
        h = '{}/{}'.format(hmm, lab)
        g = '{}/{}'.format(gpr, lab)
        gm = '{}/{}'.format(gpr_with_multi_level, lab)

        outfile = '{}/{}.eps'.format(outpath, Utility.get_basefilename(lab) )

        plot(o, h, g, gm, outfile)

        # sys.exit()

    pass
