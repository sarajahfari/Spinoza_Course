"""
-----------------------------------------------------------------------------------------
fmriprep_tmux.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run frmiprep on tmux of a server
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: bids directory
sys.argv[2]: deriv directory
sys.argv[3]: temp directory
sys.argv[4]: bids subject name (e.g. sub-001)
sys.argv[5]: server nb of threads (e.g. 8)
sys.argv[6]: use of ICA-AROMA analysis and define dimensionality(0 = NO, -1 = YES 
			 without specifying number of IC, 1-INF: YES with IC number)
-----------------------------------------------------------------------------------------
Output(s):
BIDS files
-----------------------------------------------------------------------------------------
To run:
cd to fmriprep_tmux.py folder
python fmriprep_tmux.py /home/shared/2018/visual/fMRIcourse/bids_data/7T/ 
					  	/home/shared/2018/visual/fMRIcourse/deriv_data/7T/ 
					  	/home/shared/2018/visual/fMRIcourse/temp_data/7T/fmriprep/ 
					  	sub-001
					  	8
					  	0
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
nb_thread = int(sys.argv[5])
ica_aroma_dim = int(sys.argv[6])

# define singularity and fs licence
singularity_dir = '/home/shared/software/poldracklab_fmriprep_1.1.8-2018-10-04-8958de85c5c6.img'
fs_licence = '/home/szinte/software/freesurfer/license.txt'

# server paths spinoza
#singularity_dir = '/packages/singularity_containers/poldracklab_fmriprep_latest-2017-05-21-b72da4faf69b.img'
#fs_licence = '/packages/freesurfer/6.0.0/license.txt'

# define ICA-AROMA
if ica_aroma_dim > 0: ica_aroma = "--use-aroma --aroma-melodic-dimensionality {dim:.0f}".format(dim = ica_aroma_dim)
elif ica_aroma_dim == -1: ica_aroma = "--use-aroma"
elif ica_aroma_dim == 0: ica_aroma = ""

# run singularity
singularity_cmd = "singularity run {dir} {source} {deriv_dir} participant --participant_label {sub} -w {temp} --output-space T1w fsaverage --nthreads {nb_thread:.0f} --use-syn-sdc --low-mem {ica_aroma} --fs-license-file {fs_licence}".format(  
									dir =singularity_dir, 
									source = bids_dir, 
									deriv_dir = deriv_dir,
									sub = sub,
									temp = temp_dir,
									nb_thread = nb_thread,
									ica_aroma = ica_aroma,
									fs_licence = fs_licence,
									)

# define tmux session
session_name = "{sub}_fmriprep".format(sub = sub)

# run singularity
print('run singularity on tmux {session_name}'.format(session_name = session_name))
print('to check type >> tmux a -t {session_name}'.format(session_name = session_name))
os.system("tmux new-session -d -s {session_name} '{cmd}'".format(session_name = session_name, cmd = singularity_cmd))
time.sleep(2)
