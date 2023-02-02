import numpy as np
from bmfrm import Beamformer

def rxengine(c : float, ref : np.array, points : np.array):
    """Calculate the distance from a given refernce to each point in a feild
    
    Parameters:
    ----
    `c`: the speed of sound in m/s
    `ref`: a length 3 vector containing the 3D coordinate of a given reference (element)
    `points`: a N by 3 vector containing the 3D coordinates of the desired reconstruction points

    Returns:
    ----
    `tau_rx`: an N length time delay vector in seconds
    """

    #Validate input params
    if (np.ndim(ref) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(ref) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(ref.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (not np.ndim(points) == 2) or (not points.shape[1] == 3): raise Exception("points must be a matrix with dimensions N by 3")

    ref = ref.reshape((1, 3))           # reformat the reference point for broadcasting
    points = points.reshape((-1, 3))    # reformat the spatial coordinates for broadcasting

    # calculate the physical distance between the reference and each point in the feild
    dist = np.sqrt(np.sum((points - ref)**2, axis=1))

    # convert the distance to one way time in seconds
    tau_rx = dist / c
    tau_rx = tau_rx.flatten()

    return tau_rx

def pwtxengine(c : float, tref : float, theta : float, phi : float, ref : np.array, points : np.array):
    """Calculate the time from t=0 to wave front intersection with each point
    
    Parameters:
    ----
    `c`: the speed of sound in [m/s]
    `tref`: delay tab of this reference element [s]
    `theta`: steering angle in the xz plane [radians]
    `phi`: steering angle in the yz plane [radians]
    `ref`: location of transmiting element [m, m, m]
    `points`: a N by 3 vector containing the 3D coordinates of the desired reconstruction points [N * [m, m, m]]

    Returns:
    ----
    `tau_tx`: delay tabs from t=0 to incidence with wave front
    """
    #Validate input params
    if (np.ndim(ref) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(ref) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(ref.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (not np.ndim(points) == 2) or (not points.shape[1] == 3): raise Exception("points must be a matrix with dimensions N by 3")

    # calculate location of field points relative to time shifted (delay tabs in z) reference
    points = points - ref.reshape((1, 3)) + np.array([[0, 0, c*tref]])         

    # calculate the normal vector to the plane wave
    norm = np.array([[np.sin(theta), np.sin(phi), np.cos(theta) + np.cos(phi)]])
    norm = norm / np.sqrt(np.sum(norm**2, axis = 1))

    # calculate the inner product of the normal vector and the field points to find distance to incidence
    dist = np.sum(points * norm, axis = 1)

    # convert the distance to the one way time of travel
    tau_tx = dist / c
    
    return tau_tx