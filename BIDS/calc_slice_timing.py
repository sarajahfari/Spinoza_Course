# calc_slice_timing.py
import numpy as np
sense_factor  				= 1
slice_number  				= 72
tr_duration	 				= 2.0

slice_timing = []
for repeat in np.arange(0,sense_factor,1):
	slice_timing_val = np.linspace(0,tr_duration,(slice_number/sense_factor)+1)
	slice_timing.append(slice_timing_val[:-1])
slice_timing = np.hstack(slice_timing)

print(slice_timing)