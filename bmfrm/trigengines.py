import numpy as np
from bmfrm import Beamformer

def rxengine(bmfrm : Beamformer, ref : np.array, points : np.array):
    """Calculate the distance from a given refernce to each point in a feild
    
    Parameters:
    ----
    bmfrm: beamform object containing a field 'c'
    bmfrm.c: the speed of sound in m/s
    ref: a length 3 vector containing the 3D coordinate of a given reference (element)
    points: a N by 3 vector containing the 3D coordinates of the desired reconstruction points
    Returns:
    ----
    tau_rx: an N length time delay vector in seconds
    """

    #TODO: Insert parameter validation step

    c = bmfrm.c                         # extract the speed of sound
    print(c)

    ref = ref.reshape((1, 3))           # reformat the reference point for broadcasting

    points = points.reshape((-1, 3))    # reformat the spatial coordinates for broadcasting

    # calculate the physical distance between the reference and each point in the feild
    dist = np.sqrt(np.sum((points - ref)**2, axis=1))

    # convert the distance to one way time in seconds
    tau_rx = dist / c

    tau_rx = tau_rx.flatten()

    return tau_rx