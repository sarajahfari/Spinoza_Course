"""
-----------------------------------------------------------------------------------------
fmriqc_tmux.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run frmiqc on tmux of a server
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: bids directory
sys.argv[2]: deriv directory
sys.argv[3]: temp directory
sys.argv[4]: bids subject name (e.g. sub-001)
sys.argv[5]: server nb of processor to use (e.g 4)
-----------------------------------------------------------------------------------------
Output(s):
BIDS files
-----------------------------------------------------------------------------------------
To run:
cd to fmriqc_tmux.py folder
python fmriqc_tmux.py /home/shared/2018/visual/fMRIcourse/bids_data/7T/ 
					  /home/shared/2018/visual/fMRIcourse/deriv_data/7T/ 
					  /home/shared/2018/visual/fMRIcourse/temp_data/7T/mriqc/ 
					  sub-001
					  8
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import sys
import os
import time
opj = os.path.join

# inputs
bids_dir = sys.argv[1]
deriv_dir = sys.argv[2]
temp_dir = sys.argv[3]
sub = sys.argv[4]
nb_procs = int(sys.argv[5])

# define singularity and fs licence
singularity_dir = '/home/shared/software/poldracklab_mriqc_0.11.0-2018-06-05-442554ee49a6.img'

# run singularity
singularity_cmd = "singularity run {dir} {source} {deriv_dir} participant --participant_label {sub} -w {temp} --n_procs {nb_procs:.0f} --verbose-reports --mem_gb 64 -m bold T1w T2w --no-sub".format(
									dir =singularity_dir, 
									source = bids_dir, 
									deriv_dir = deriv_dir,
									sub = sub,
									temp = temp_dir,
									nb_procs = nb_procs,
									)

# define tmux session
session_name = "{sub}_fmriqc".format(sub = sub)

# run singularity
print('run singularity on tmux {session_name}'.format(session_name = session_name))
print('to check type >> tmux a -t {session_name}'.format(session_name = session_name))

os.system("tmux new-session -d -s {session_name} '{cmd}'".format(session_name = session_name, cmd = singularity_cmd))
time.sleep(2)