
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import re
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    result_path = '/work/w25/decha/decha_w25/ICASSP_2017_workspace/Products_of_Gaussian/Playground/result.txt'

    pattern = re.compile(r""".+RMSE:\s(?P<rmse>.+)\sin.+""",re.VERBOSE)

    for line in Utility.read_file_line_by_line(result_path):

        if 'phones' not in line: 
            p = Utility.trim(line)
        else:
            match = re.match(pattern, line)
            if match:   
                rmse = match.group('rmse')
                # if 24.504268 > float(rmse):
                if 24.504162 > float(rmse):
                    print p
                    print 'RMSE:', rmse

    pass
