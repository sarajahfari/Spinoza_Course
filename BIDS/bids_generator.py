"""
-----------------------------------------------------------------------------------------
bids_generator.py
-----------------------------------------------------------------------------------------
Goal of the script:
Convert data in BIDS format
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: raw data folder
sys.argv[2]: bids folder
sys.argv[3]: subject bids number (e.g. sub-001)
sys.argv[4]: task name
-----------------------------------------------------------------------------------------
Output(s):
BIDS files
-----------------------------------------------------------------------------------------
To run:
ssh -Y compute-01
module load collections/default
cd /data1/projects/fMRI-course/Spinoza_Course/
python bids_generator.py [raw data path] [bids data path] [subject name] [task name]
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import sys
import os
import glob
import nibabel as nb
opj = os.path.join

# inputs
raw_dir = sys.argv[1]
bids_dir =  sys.argv[2]
sub_name_bids =  sys.argv[3]
task_name =  sys.argv[4]

# define data transfer command
trans_cmd = 'rsync -avuz --progress'

# create bids folders
for bids_folder in ['anat','fmap','func']:
	exec("{bids_folder}_dir = opj(bids_dir,sub_name_bids,'{bids_folder}')".format(bids_folder = bids_folder))
	try: exec("os.makedirs({}_dir)".format(bids_folder))
	except: pass

# BIDS /anat
# ----------
# T1w
t1w_raw = glob.glob(opj(raw_dir,'nifti','*T1*'))[0]
t1w_bids = opj(anat_dir,"{}_T1w.nii.gz".format(sub_name_bids))
os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = t1w_raw, dest = t1w_bids))

# BIDS /fmap
# ----------
# B0 magnitude
b0_magnitude_raw = glob.glob(opj(raw_dir,'nifti','*magnitude*')) # if conversion using parrec2nii
if len(b0_magnitude_raw)==0: # if conversion using dcm2niix
	b0_magnitude_raw = glob.glob(opj(raw_dir,'nifti','*B0*'))
	b0_magnitude_raw = [fn for fn in b0_magnitude_raw if 'real' not in fn]

b0_magnitude_bids = opj(fmap_dir,"{}_magnitude1.nii.gz".format(sub_name_bids))
os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = b0_magnitude_raw[0], dest = b0_magnitude_bids))

# B0 phasediff
b0_phasediff_raw = glob.glob(opj(raw_dir,'nifti','*phasediff*')) # if conversion using parrec2nii
if len(b0_phasediff_raw)==0: # if conversion using dcm2niix
	b0_phasediff_raw = glob.glob(opj(raw_dir,'nifti','*real*'))
b0_phasediff_bids = opj(fmap_dir,"{}_phasediff.nii.gz".format(sub_name_bids))
os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = b0_phasediff_raw[0], dest = b0_phasediff_bids))

# BIDS /func
# ----------
# bold runs
bold_runs_raw = glob.glob(opj(raw_dir,'nifti','*bold*'))
if len(bold_runs_raw)==0:
	bold_runs_raw = glob.glob(opj(raw_dir,'nifti','*FN*'))
if len(bold_runs_raw)==0:
	bold_runs_raw = glob.glob(opj(raw_dir,'nifti','*run*'))
# add another line here if your raw data does not contain any of the above names

for run_num,bold_run_raw in enumerate(bold_runs_raw):	
	bold_run_bids = opj(func_dir,"{sub}_task-{task}_run-{run:.0f}_bold.nii.gz".format(sub = sub_name_bids, task = task_name, run = run_num+1))
	os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = bold_run_raw, dest = bold_run_bids))

# events runs
events_runs_raw = glob.glob(opj(raw_dir,'*events*'))
for run_num,events_run_raw in enumerate(events_runs_raw):
	events_run_bids = opj(func_dir,"{sub}_task-{task}_run-{run:.0f}_events.tsv".format(sub = sub_name_bids, task = task_name, run = run_num+1))
	os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = events_run_raw, dest = events_run_bids))
