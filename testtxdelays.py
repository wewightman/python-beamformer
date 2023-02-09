import numpy as np
import matplotlib.pyplot as plt
import bmfrm.trigengines as trig

c=1540
fnum=2
indsel = 31
dele = 0.298E-3
focalrx = 30E-3
focaltx = 28E-3
nele = 128
x = dele * (np.arange(nele) - (nele-1)/2)
y = 0
z = 0
X, Y, Z = np.meshgrid(x, y, z, indexing='xy')
eles = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T

focus = np.array([[dele*(indsel-(nele-1)/2), 0, focaltx]])
dt_tx, mask_tx = trig.dtbyele(c, fnum, focus, eles)
dt_tx[~mask_tx] = 0
focus = np.array([[dele*(indsel-(nele-1)/2), 0, focalrx]])
dt_rx, mask_rx = trig.dtbyele(c, fnum, focus, eles)
dt_rx[~mask_rx] = 0

plt.figure()
plt.plot(dt_tx)
plt.plot(dt_rx)
plt.plot(dt_tx+dt_rx)
plt.plot(dt_rx+np.max(dt_tx))
plt.show()
