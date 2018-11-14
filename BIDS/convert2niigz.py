"""
-----------------------------------------------------------------------------------------
convert2niigz.py
-----------------------------------------------------------------------------------------
Goal of the script:
Convert PAR/REC to nifti (nii.gz) format and separate B0 file in phasediff and magnitude
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: input folder directory
-----------------------------------------------------------------------------------------
Output(s):
nifti files
-----------------------------------------------------------------------------------------
To run:
cd to convert2niigz.py folder
python convert2niigz.py '/home/shared/2018/visual/fMRIcourse/raw_data/pilot/'
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

# define subject folder
input_folder = sys.argv[1]

# create output folder
output_folder = opj(input_folder,'nifti')
try: os.makedirs(output_folder)
except: pass

# get PAR REC file list
list_par_files = glob.glob(opj(input_folder,'*.PAR'))

# convert files
print('convert files to nifti')
for par_file in list_par_files:
	print(par_file)
	cmd_txt = "parrec2nii --compressed -c --overwrite --store-header -o {out} {par}".format(out = output_folder, par = par_file)
	os.system(cmd_txt)

# separate b0 magnitude and phasediff files
b0_file = glob.glob(opj(output_folder,'*B0*'))
b0_load = nb.load(b0_file[0])

b0_data = b0_load.get_data()
for typeB0num, typeB0 in enumerate(['magnitude','phasediff']):
	out_img = nb.Nifti1Image(dataobj = b0_data[...,typeB0num], affine = b0_load.affine, header = b0_load.header)
	out_img.to_filename(b0_file[0][:-7]+"_{}.nii.gz".format(typeB0))
