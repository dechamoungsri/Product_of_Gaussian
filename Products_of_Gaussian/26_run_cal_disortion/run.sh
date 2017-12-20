#!/bin/sh

setenv PATH /usr/local/MATLAB/R2015a/bin:/usr/local/bin:/home/h1/koriyama/tool/SPTK/SPTK-3.8/bin.Linux.x86_64/bin:/home/h1/koriyama/tool/HTS/HTS-2.3/htk/bin.Linux.x86_64/bin/:$PATH

setenv LANG C

setenv LC_ALL en_US.UTF-8

tone=0

/usr/local/bin/python -u ./run_cal_distortion.py -t $tone -b 0.3 -p /work/w21/decha/Interspeech_2017/Result/C3-250-frame-utterance-02-train-all-unstress-stress/Syllable_training_size_950/block_size_256/num_coeff_4/tone_$tone/

echo '------------------------------------------'

tone=1

/usr/local/bin/python -u ./run_cal_distortion.py -t $tone -b 0.1 -p /work/w21/decha/Interspeech_2017/Result/C3-250-frame-utterance-02-train-all-unstress-stress/Syllable_training_size_950/block_size_256/num_coeff_4/tone_$tone/

echo '------------------------------------------'

tone=2

/usr/local/bin/python -u ./run_cal_distortion.py -t $tone -b 0.1 -p /work/w21/decha/Interspeech_2017/Result/C3-250-frame-utterance-02-train-all-unstress-stress/Syllable_training_size_950/block_size_256/num_coeff_4/tone_$tone/

echo '------------------------------------------'

tone=3

/usr/local/bin/python -u ./run_cal_distortion.py -t $tone -b 0.1 -p /work/w21/decha/Interspeech_2017/Result/C3-250-frame-utterance-02-train-all-unstress-stress/Syllable_training_size_950/block_size_256/num_coeff_4/tone_$tone/

echo '------------------------------------------'

tone=4

/usr/local/bin/python -u ./run_cal_distortion.py -t $tone -b 0.3 -p /work/w21/decha/Interspeech_2017/Result/C3-250-frame-utterance-02-train-all-unstress-stress/Syllable_training_size_950/block_size_256/num_coeff_4/tone_$tone/