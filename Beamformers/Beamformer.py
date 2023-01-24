
import numpy as np
class Beamformer:
    """Class object defining a beamformer. Needs the following parameters defined...

    Parameters:
    ----
    Nt: number of time samples per RF line (int)
    dt: sampling period of channel data [s]
    tstart: start time of rf line [s]
    usf: upsample factor (int) newsamples/old
    nele: number of elements in transducer
    dele: element pitch [m]
    Nlat: number of lateral, reconstructed pixels (int)
    dlat: lateral spacing of pixels [m]
    Nax: number of axial pixels (int)
    dax: spacing between axial pixels [m]
    ulc: spatial location of upper left corner [m, m]
    apod: apodization function (default None)
    fnum: fnumber used in recon (default None)
    """
    def __init__(self):
        """Initialize the beamformer with needed parameters"""
        self.Nt = None
        self.dt = None
        self.tstart = None
        self.usf = None
        self.nele = None
        self.dele = None
        self.Nlat = None
        self.dlat = None
        self.Nax = None
        self.dax = None
        self.ulc = None
        self.apod = None
        self.fnum = None

    def verifyparams(self):
        """Verify parameters. Should be called after all required feilds are filled"""
        pass

    def gentabs(self):
        # Verify this beamformer has been instantiated properly
        print(getattr(self,'Nt'))

        # Calculate the lateral position of elements, and the axial/lateral coordinates of recon pixels
        self.posele = np.linspace(-self.dele*(self.nele-1)/2, self.dele*(self.nele-1)/2, self.nele)
        self.posax = np.linsapce(self.ulc[0], self.ulc[0] + self.Nax*self.dax, self.Nax)
        self.poslat = np.linsapce(self.ulc[1], self.ulc[1] + self.Nlat*self.dlat, self.Nlat)
        self.t = self.tstart + self.dt * np.arange(self.Nt*self.usf + 1) / self.usf # one additional data point to set to zero

    def __str__(self):
        return "ooooooooops"

oop = Beamformer()

print(oop.Nt)
oop.Nt = int(3)
print(oop.Nt)
print(oop)
