#!/bin/tcsh

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 0 0.1 2.0 no_plot stress_only >! ./log_F/log_3-256-950-0.txt &
/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 1 0.1 2.0 no_plot stress_only >! ./log_F/log_3-256-950-1.txt &
/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 2 0.1 2.0 no_plot stress_only >! ./log_F/log_3-256-950-2.txt &
/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 3 0.1 2.0 no_plot stress_only >! ./log_F/log_3-256-950-3.txt &
/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 4 0.1 2.0 no_plot stress_only >! ./log_F/log_3-256-950-4.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 0 0.5 0.6 no_plot stress_only >! ./log_F/log_3-256-950-0-0.5-0.6.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 0 0.7 2.0 no_plot stress_only >! ./log_F/log_3-256-950-0-0.7-2.0.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 1 1.9 2.0 no_plot stress_only >! ./log_F/log_3-256-950-1-1.9-2.0.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 2 0.7 2.0 no_plot stress_only >! ./log_F/log_3-256-950-2-0.7-2.0.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 3 1.3 2.0 no_plot stress_only >! ./log_F/log_3-256-950-3-1.3-2.0.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 4 0.1 2.0 no_plot stress_only >! ./log_F/log_3-256-950-4.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 2 0.9 2.0 no_plot stress_only > ! ./log_F/log_3-256-950-2-0.9-2.0.txt &

/usr/local/bin/python -u ./run_joint_optimal_for_beta_gamma.py 3 256 950 2 1.1 2.0 no_plot stress_only > ! ./log_F/log_3-256-950-2-1.1-2.0.txt &
