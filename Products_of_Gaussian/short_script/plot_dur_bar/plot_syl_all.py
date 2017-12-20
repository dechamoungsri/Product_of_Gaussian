
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

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
    fig.set_size_inches(len(ind) * 8 / 10 , 6)

    f, ax = plt.subplots(3, sharex=True, sharey=True)

    for dur_idx, dur_path in enumerate( [hmm, gpr, gpr_with_multi_level] ): 

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

            syl_dur_list.append( float(phone_sum - ori_sum)/50000.0 )

            syllable_position.append(count)

        # print 'Length : ', len(phone_dur_list), len(ind)

        # ax[dur_idx].bar(ind, phone_dur_list,color=colors[dur_idx])

        ind = np.arange( len(syl_dur_list) )
        ax[dur_idx].bar(ind, syl_dur_list,color=colors[dur_idx])

        # for s in syllable_position:
        #     # print s
        #     ax[dur_idx].plot([s, s], ax[dur_idx].get_ylim(), 'k--', lw=0.5)

        plt.savefig(outfile)
        

    pass

if __name__ == '__main__':

    org = '/work/w2/decha/Data/GPR_speccom_data/mono_to_syl_dur/'
    hmm = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/01_GPR/mono_to_syl_dur/'
    gpr = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/02_GPR_with_multi_level/mono_to_syl_dur/'
    gpr_with_multi_level = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/mono_label/03_PoG/mono_to_syl_dur/'

    outpath = './dur_distortion_syl/'
    Utility.make_directory(outpath)

    for lab in Utility.list_file(org):
        print lab

        o = '{}/{}'.format(org, lab)
        h = '{}/{}'.format(hmm, lab)
        g = '{}/{}'.format(gpr, lab)
        gm = '{}/{}'.format(gpr_with_multi_level, lab)

        outfile = '{}/{}.eps'.format(outpath, Utility.get_basefilename(lab) )

        plot(o, h, g, gm, outfile)

        # sys.exit()

    pass
