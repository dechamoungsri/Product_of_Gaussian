#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

/usr/local/bin/python -u ./run_three_optimal.py 3 256 250 0 0.1 2.0 no_plot stress_only >! ./log_C5_new/log_3-256-250-0.txt 

/usr/local/bin/python -u ./run_three_optimal.py 3 256 250 1 0.1 2.0 no_plot stress_only >! ./log_C5_new/log_3-256-250-1.txt 

/usr/local/bin/python -u ./run_three_optimal.py 3 256 250 2 0.1 2.0 no_plot stress_only >! ./log_C5_new/log_3-256-250-2.txt 

/usr/local/bin/python -u ./run_three_optimal.py 3 256 250 3 0.1 2.0 no_plot stress_only >! ./log_C5_new/log_3-256-250-3.txt 

/usr/local/bin/python -u ./run_three_optimal.py 3 256 250 4 0.1 2.0 no_plot stress_only >! ./log_C5_new/log_3-256-250-4.txt 