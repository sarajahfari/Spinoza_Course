import nibabel as nb

file_dir = '/home/shared/2018/visual/fMRIcourse/bids_data/7T/sub-001/func/sub-001_task-StopSignal_run-1_bold.nii.gz'
load_file =  nb.load(file_dir)

header = load_file.header
affine = load_file.affine
data = load_file.get_data()
header['pixdim'][4] = header['pixdim'][4]*1000


img = nb.Nifti1Image(data, affine=affine, header=header)
img.to_filename(file_dir)