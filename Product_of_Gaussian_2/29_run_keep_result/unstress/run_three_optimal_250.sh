#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

mkdir -p log_Exp_1

set now=`date +"%T"`

echo $now

/usr/local/bin/python -u ./three_level_running_unstress_250.py ./log_Exp_1/ >! ./log_Exp_1/log.unstress.$now.txt

echo 'panda End'