#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

mkdir -p log_Exp_1_fix

set training_size=450

# set tone=0
# /usr/local/bin/python -u ./run_joint_main.py -startbeta 1.3 -endbeta 1.4 -tone $tone -stress_or_unstress unstress -use_partial_coeff -num_coeff 3 -block_size 256 -training_size $training_size >! ./log_Exp_1_fix/log.tone.$tone.$training_size.txt 

# set tone=4
# /usr/local/bin/python -u ./run_joint_main.py -startbeta 0.5 -endbeta 0.6 -tone $tone -stress_or_unstress unstress -use_partial_coeff -num_coeff 3 -block_size 256 -training_size $training_size >! ./log_Exp_1_fix/log.tone.$tone.$training_size.txt 


set training_size=250

# set tone=0
# /usr/local/bin/python -u ./run_joint_main.py -startbeta 1.7 -endbeta 1.8 -tone $tone -stress_or_unstress unstress -use_partial_coeff -num_coeff 3 -block_size 256 -training_size $training_size >! ./log_Exp_1_fix/log.tone.$tone.$training_size.txt 


# set tone=2
# /usr/local/bin/python -u ./run_joint_main.py -startbeta 0.3 -endbeta 0.4 -tone $tone -stress_or_unstress unstress -use_partial_coeff -num_coeff 3 -block_size 256 -training_size $training_size >! ./log_Exp_1_fix/log.tone.$tone.$training_size.txt 


set tone=4
/usr/local/bin/python -u ./run_joint_main.py -startbeta 1.1 -endbeta 1.2 -tone $tone -stress_or_unstress unstress -use_partial_coeff -num_coeff 3 -block_size 256 -training_size $training_size >! ./log_Exp_1_fix/log.tone.$tone.$training_size.txt 
