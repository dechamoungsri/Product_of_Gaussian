#!/bin/tcsh

/usr/local/bin/python -u ./run_joint_prob.py 4 256 950 0 >! log_4-256-950-0.txt &

/usr/local/bin/python -u ./run_joint_prob.py 4 256 950 1 >! log_4-256-950-1.txt &

/usr/local/bin/python -u ./run_joint_prob.py 4 256 950 2 >! log_4-256-950-2.txt &

/usr/local/bin/python -u ./run_joint_prob.py 4 256 950 3 >! log_4-256-950-3.txt &

/usr/local/bin/python -u ./run_joint_prob.py 4 256 950 4 >! log_4-256-950-4.txt &

