#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

set today=`date '+%Y_%m_%d'`

set phone_type=vowel

set log='./log_phone_and_syllable_'$today'_'$phone_type'_'tone_all'/'

mkdir -p $log

set tone=2

/usr/local/bin/python -u ./run.py \
-method_name Stress_Method_C_phone_syllable_tone_separated \
-mainoutpath /work/w21/decha/Interspeech_2017/Result_3/ \
-start_ph_1toN 1.0 -end_ph_1toN 3.0 \
-start_ph_0 0.0 -end_ph_0 0.5 \
-start_syl_1toN 1.0 -end_syl_1toN 2.0 \
-start_syl_0 0.0 -end_syl_0 0.5 \
-increment 0.1 \
-phone_type $phone_type \
-training_size 250 -tone $tone -stress_type 1 -tone_folder all >! ./$log/log_ph_C_tone_$tone'.txt'
