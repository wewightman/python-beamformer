import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import h5py as h5

import bmfrm.Beamformer as Beamformer

filepw = "C:\\Users\\14142\\OneDrive - Duke University\\Classes\\RIP\\Ultrasound\\unfocused_transmit1.mat"
filefoc = "C:\\Users\\14142\\OneDrive - Duke University\\Classes\\RIP\\Ultrasound\\focused_transmit1.mat"

with h5.File(filepw, ) as f:
    datapw = np.array(f['rf'])

with h5.File(filefoc, 'r') as f:
    datafoc = np.array(f['rf'])

env = np.abs(sig.hilbert(datafoc[64,:,:].T, axis=0))
logged = 20*np.log10(env/np.percentile(env, 99))

plt.figure(1)
plt.imshow(logged, vmin=-40, vmax=0, aspect=0.1)
plt.show()

