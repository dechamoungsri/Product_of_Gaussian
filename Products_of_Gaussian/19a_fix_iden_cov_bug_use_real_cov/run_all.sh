#!/bin/csh

/usr/local/bin/python -u ./run_joint_prob_all_tone.py 3 256 950 all 0.1 2.0 >! log_3-256-950-all.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 0 >! log_3-256-950-0.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 1 >! log_3-256-950-1.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 2 >! log_3-256-950-2.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 3 >! log_3-256-950-3.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 4 >! log_3-256-950-4.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 0 2.1 4.0 >! log_3-256-950-0-21-40.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 1 0.1 2.0 plot >! log_3-256-950-1-plot.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 3 0.1 2.0 plot >! log_3-256-950-3-plot.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 1 1.9 2.0 plot >! log_3-256-950-1-plot.txt &

/usr/local/bin/python -u ./run_joint_prob_tone_from_all_no_plot.py 3 256 950 3 1.9 2.0 plot >! log_3-256-950-3-plot.txt &

/usr/local/bin/python -u ./run_joint_main.py 4 256 950 0 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-0.txt &
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 1 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-1.txt &
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 2 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-2.txt &
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 3 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-3.txt &
/usr/local/bin/python -u ./run_joint_main.py 4 256 950 4 0.1 2.0 no_plot no_stress_only >! ./log_E/log_4-256-950-4.txt &

/usr/local/bin/python -u ./run_joint_main.py 3 256 950 4 1.5 1.6 plot stress_only >! ./log_C_log_4-256-950-4-15-16.txt &