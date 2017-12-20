#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

mkdir -p log_C2_250_plot

/usr/local/bin/python -u ./run_small_data.py 3 256 250 0 2.9 3.0 plot stress_only use_partial_coeff >! ./log_C2_250_plot/log_3-256-250-0.txt 
# /usr/local/bin/python -u ./run_small_data.py 3 256 250 1 0.1 0.2 plot stress_only use_partial_coeff >! ./log_C2_250_plot/log_3-256-250-1.txt 
/usr/local/bin/python -u ./run_small_data.py 3 256 250 2 1.1 1.2 plot stress_only use_partial_coeff >! ./log_C2_250_plot/log_3-256-250-2.txt 
/usr/local/bin/python -u ./run_small_data.py 3 256 250 3 0.9 1.0 plot stress_only use_partial_coeff >! ./log_C2_250_plot/log_3-256-250-3.txt 
/usr/local/bin/python -u ./run_small_data.py 3 256 250 4 1.3 1.4 plot stress_only use_partial_coeff >! ./log_C2_250_plot/log_3-256-250-4.txt 
