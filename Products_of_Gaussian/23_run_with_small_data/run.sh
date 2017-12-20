/usr/local/bin/python -u ./cal_small_data_distortion.py 3 256 950 4 0.0 1.0

/usr/local/bin/python -u ./run_small_data.py 3 256 950 0 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2/log_3-256-950-0.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 950 1 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2/log_3-256-950-1.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 950 2 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2/log_3-256-950-2.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 950 3 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2/log_3-256-950-3.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 950 4 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2/log_3-256-950-4.txt &

/usr/local/bin/python -u ./run_small_data.py 3 256 250 0 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2_250/log_3-256-250-0.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 250 1 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2_250/log_3-256-250-1.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 250 2 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2_250/log_3-256-250-2.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 250 3 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2_250/log_3-256-250-3.txt &
/usr/local/bin/python -u ./run_small_data.py 3 256 250 4 0.1 2.0 no_plot stress_only use_partial_coeff >! ./log_C2_250/log_3-256-250-4.txt &

/usr/local/bin/python -u ./run_small_data.py 3 256 250 0 2.1 4.0 no_plot stress_only use_partial_coeff >! ./log_C2_250/log_3-256-250-0-2.1-4.0.txt &
