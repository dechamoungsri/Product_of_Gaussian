#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

/usr/local/bin/python -u ./run_joint_main.py 4 256 950 0 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-0.txt 
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 1 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-1.txt 
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 2 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-2.txt 
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 3 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-3.txt 
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 4 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-4.txt 