#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

mkdir -p log_Exp_2

set num_coeff=1
set training_size=450

set tone=0
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=1
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=2
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=3
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=4
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set training_size=250

set tone=0
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=1
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=2
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=3
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 

set tone=4
/usr/local/bin/python -u ./run_joint_main.py -startbeta 0.1 -endbeta 2.0 -tone $tone -stress_or_unstress unstress -num_coeff $num_coeff -block_size 256 -training_size $training_size >! ./log_Exp_2/log.tone.$tone.$training_size.txt 
