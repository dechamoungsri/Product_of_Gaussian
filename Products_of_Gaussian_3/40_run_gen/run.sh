#!/bin/tcsh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

/usr/local/bin/python -u ./run.py \

-method_name Method_A_phone
-mainoutpath /work/w21/decha/Interspeech_2017/Result_2/

-start_ph_1toN 1.7 -end_ph_1toN 1.8 \
-start_ph_0 0.9 -end_ph_0 1.0 \

-start_syl_1toN 0.0 -end_syl_1toN 0.1 \
-start_syl_0 0.0 -end_syl_0 0.1 \

-training_size 250 -tone 4 -stress_type 1 -tone_folder all >! log_ph.test.txt

# /usr/local/bin/python -u ./run.py \
# -start_syl_1toN 1.1 -end_syl_1toN 1.2 \
# -start_syl_0 0.0 -end_syl_0 0.1 \
# -training_size 250 -tone 2 -stress_type 1 -tone_folder all >! log_1.1_0.0.txt
