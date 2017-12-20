#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

mkdir -p ./log/

set tone=4

/usr/local/bin/python -u ./run.py \
-method_name Stress_Method_B_phone_syllable \
-mainoutpath /work/w21/decha/Interspeech_2017/Result_2/ \
-start_ph_1toN 0.0 -end_ph_1toN 2.0 \
-start_ph_0 0.0 -end_ph_0 2.0 \
-start_syl_1toN 0.0 -end_syl_1toN 2.0 \
-start_syl_0 0.0 -end_syl_0 2.0 \
-training_size 250 -tone $tone -stress_type 1 -tone_folder all >! ./log/log_ph_B_tone_$tone.txt