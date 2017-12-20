
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

import numpy as np

import re

if __name__ == '__main__':

    outpath = '/work/w2/decha/Data/GPR_speccom_data/01_phone_level_data/stress_list/j/'

    Utility.make_directory(outpath)

    for num in range(1, 51):

        name = 'tscsdj{}'.format(Utility.fill_zero(num, 2))

        filename = '/work/w2/decha/Data/GPR_speccom_data/full_time_with_stress/tsc/sd/j/{}.lab'.format( name )

        pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+\-(?P<phone_position>.+)_.+\+.+/B:.+\-(?P<tone>.+)\+.+/C:.+/I:.+\-(?P<stress>.+)\+.+""",re.VERBOSE)
        lines = Utility.read_file_line_by_line(filename)

        out = []

        for line in lines:
            # print line
            match = re.match(pattern, line)
            if match:
               phone = match.group('curphone')
               phone_position = match.group('phone_position')
               tone = match.group('tone')
               stress = match.group('stress')

               if phone_position != 'x':
                    phone_position = int(phone_position)-1

               o = [stress, tone, phone_position]
               out.append(o)

               # print phone, phone_position, tone, stress

        # print out

        if len(out) != len(lines):
            print filename

        outpath_file = '{}/{}.npy'.format(outpath, name)

        np.save(outpath_file, out)

    pass
