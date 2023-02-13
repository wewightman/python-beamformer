import numpy as np

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

    # calculate the physical distance between the reference and each point in the feild
    dist = np.sqrt(np.sum((points - ref)**2, axis=1))

    # convert the distance to one way time in seconds
    tau_rx = dist / c

    return tau_rx.flatten()

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
    norm = np.array([[np.sin(theta), np.sin(phi), np.cos(theta) * np.cos(phi)]])
    norm = norm / np.sqrt(np.sum(norm**2, axis = 1))

    # calculate the inner product of the normal vector and the field points to find distance to incidence
    dist = np.sum(points * norm, axis = 1)

    # convert the distance to the one way time of travel
    tau_tx = dist / c

    return tau_tx.flatten()

def foctxengine(c : float, tref : float, focal : np.array, ref : np.array, points : np.array):
    """Calculate time from t=0 to points intersection with wavefront

    Parameters:
    ----
    `c`: the speed of sound in [m/s]
    `tref`: delay tab of this reference element [s]
    `focus`: focus point of transmist - can be in front of or behind transducer
    `ref`: location of transmiting element [m, m, m]
    `points`: a N by 3 vector containing the 3D coordinates of the desired reconstruction points [N * [m, m, m]]

    Returns:
    ----
    `tau_tx`: delay tabs from t=0 to incidence with wave front
    """

    # validate inputs
    if (np.ndim(focal) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(focal) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(focal.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (np.ndim(ref) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(ref) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(ref.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (not np.ndim(points) == 2) or (not points.shape[1] == 3): raise Exception("points must be a matrix with dimensions N by 3")
    
    # calculate location of field points relative to time shifted (delay tabs in z) reference
    points = points - ref.reshape((1, 3)) - np.array([[0, 0, c*tref]])         

    # calculate the normal vector to the plane wave
    norm = np.array([[0, 0, 1]])

    # calculate the inner product of the normal vector and the field points to find distance to incidence
    dist = np.sum(points * norm, axis = 1)

    # convert the distance to the one way time of travel
    tau_tx = dist / c

    return tau_tx.flatten()

def dtbyele(c : float, fnum : float, focus : np.array, eles : np.array, theta = float(0), phi = float(0)):
    """Calculate the delay tabs for each element for a given focal point, fnumber, and steering angles
    
    Parameters:
    ----
    `c`: speed of sound [m/s]
    `fnum`: fnumber of apperature
    `focus`: 1 by 3 numpy array containing coordinates of focus [m, m, m]
    `eles`: spatial location of N elements N by 3 [N*[m, m, m]]
    FIXME: Implement steering function

    Returns:
    ----
    `dt`: delay tabs for each element
    `mask`: mask of elements included in the apodization
    """
    # validate params
    if (np.ndim(focus) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(focus) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(focus.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (not np.ndim(eles) == 2) or (not eles.shape[1] == 3): raise Exception("points must be a matrix with dimensions N by 3")

    # FIXME: Find centerpoint of focus with steering, for now assumed x,y position
    ref = focus * np.array([[1, 1, 0]])

    # make a mask to select the active elements (as defined by the f number)
    halfdiam = np.sqrt(np.sum((eles*np.array([[1, 1, 0]]) - ref)**2, axis = 1))
    
    # 2*fnum >= focus[z]/halfdiam --> 2*halfdiam >= focus[z]/fnum
    mask = np.zeros(eles.shape[0], dtype=bool)
    mask[2*halfdiam <= focus[0,2]/fnum] = True
    
    # find distances from each element to each point
    dist = np.sqrt(np.sum((eles-focus)**2, axis = 1))
    dt = (np.max(dist[mask])-dist)/c
    
    return dt, mask