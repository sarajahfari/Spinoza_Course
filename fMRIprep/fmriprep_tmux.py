"""
-----------------------------------------------------------------------------------------
fmriprep_tmux.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run frmiprep on tmux of a server
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: main data directory to mount in singularity (e.g. data1)
sys.argv[2]: bids directory
sys.argv[3]: deriv directory
sys.argv[4]: temp directory
sys.argv[5]: bids subject name (e.g. sub-001)
sys.argv[6]: server nb of threads (e.g. 8)
sys.argv[7]: your name to create your tmux session (e.g. student01)
-----------------------------------------------------------------------------------------
Output(s):
Preprocessed data and confound regressors in deriv directory
-----------------------------------------------------------------------------------------
To run:
ssh -Y compute-01
module load collections/default
cd /data1/projects/fMRI-course/Spinoza_Course/fMRIprep/
python fmriprep_tmux.py [main directory] [bids directory] [deriv directory] [temp directory]
						[subject] [processessors] [your id]
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import sys
import os
import time

# inputs
main_dir = sys.argv[1]
bids_dir = sys.argv[2]
deriv_dir = sys.argv[3]
temp_dir = sys.argv[4]
sub = sys.argv[5]
nb_thread = int(sys.argv[6])
your_id = sys.argv[7]

# define singularity and fs licence
singularity_dir = '/packages/singularity_containers/poldracklab_fmriprep_1.1.8-2018-10-04-8958de85c5c6.img'
fs_licence = '/data1/projects/fMRI-course/Spinoza_Course/license.txt'

# run singularity
singularity_cmd = "singularity run --bind /{main_dir}:/{main_dir} {dir} {source} {deriv_dir} participant --participant_label {sub} -w {temp} --output-space T1w template fsaverage --nthreads {nb_thread:.0f} --use-syn-sdc --low-mem --fs-license-file {fs_licence} --no-submm-recon --fs-no-reconall".format(  
									main_dir = main_dir,
									dir =singularity_dir, 
									source = bids_dir, 
									deriv_dir = deriv_dir,
									sub = sub,
									temp = temp_dir,
									nb_thread = nb_thread,
									fs_licence = fs_licence,
									)

# define tmux session
session_name = "{id}_{sub}_fmriprep".format(id = your_id, sub = sub)

# run singularity
print('run singularity on tmux {session_name}'.format(session_name = session_name))
print('to check type >> tmux a -t {session_name}'.format(session_name = session_name))
print('to run manually >> {cmd}'.format(cmd = singularity_cmd))

os.system("tmux new-session -d -s {session_name} '{cmd}'".format(session_name = session_name, cmd = singularity_cmd))
time.sleep(2)
