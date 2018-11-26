"""
-----------------------------------------------------------------------------------------
mriqc_tmux.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run frmiqc on tmux of a server
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: main data directory to mount in singularity (e.g. data1)
sys.argv[2]: bids directory
sys.argv[3]: deriv directory
sys.argv[4]: temp directory
sys.argv[5]: bids subject name (e.g. sub-001)
sys.argv[6]: server nb of processor to use (e.g 4)
-----------------------------------------------------------------------------------------
Output(s):
BIDS files
-----------------------------------------------------------------------------------------
To run:
ssh -Y compute-01
module load collections/default
cd /data1/projects/fMRI-course/Spinoza_Course/
python mriqc_tmux.py [main directory] [bids directory] [deriv directory] [temp directory] 
					 [subject] [processessors]
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
main_dir = sys.argv[1]
bids_dir = sys.argv[2]
deriv_dir = sys.argv[3]
temp_dir = sys.argv[4]
sub = sys.argv[5]
nb_procs = int(sys.argv[6])

# define singularity and fs licence
singularity_dir = '/packages/singularity_containers/poldracklab_mriqc_0.11.0-2018-06-05-442554ee49a6.img'

# run singularity
singularity_cmd = "singularity run --bind /{main_dir}:/{main_dir} {dir} {source} {deriv_dir} participant --participant_label {sub} -w {temp} --n_procs {nb_procs:.0f} --verbose-reports --mem_gb 64 -m bold T1w --no-sub".format(
									main_dir = main_dir,
									dir =singularity_dir, 
									source = bids_dir, 
									deriv_dir = deriv_dir,
									sub = sub,
									temp = temp_dir,
									nb_procs = nb_procs,
									)

# define tmux session
session_name = "{sub}_mriqc".format(sub = sub)

# run singularity
print('run singularity on tmux {session_name}'.format(session_name = session_name))
print('to run manually >> {cmd}'.format(cmd = singularity_cmd))
print('to check on tmux type >> tmux a -t {session_name}'.format(session_name = session_name))

os.system("tmux new-session -d -s {session_name} '{cmd}'".format(session_name = session_name, cmd = singularity_cmd))
time.sleep(2)
