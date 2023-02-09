import numpy as np

def genmask(fnum : float, ref : np.array, focus : np.array, points : np.array, dynamic=True):
    """Generate apodization masks

    Parameters:
    ----
    `fnum`: fnumber of transmission
    `ref`: location of transmiting element [m, m, m]
    `focus`: focus point of transmist - z component of normal vector of (focus - ref) > 0
    `points`: a N by 3 vector containing the 3D coordinates of the desired reconstruction points [N * [m, m, m]]
    `dynamic`: flag to use dynamic or fixed apodization

    Returns:
    ----
    `apod`: apodization mask
    """

    # validate inputs
    if (np.ndim(focus) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(focus) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(focus.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (np.ndim(ref) < 1): raise Exception("ref must be a vector of length 3")
    if (np.ndim(ref) > 2): raise Exception("ref must be a vector of length 3")
    if (not np.prod(ref.shape) == 3): raise Exception("ref must be a vector of length 3")
    if (not np.ndim(points) == 2) or (not points.shape[1] == 3): raise Exception("points must be a matrix with dimensions N by 3")
    
    # Calculate the normal vector along steering angle
    focus = focus.reshape((1, 3))
    ref = ref.reshape((1,3))
    norm = (focus-ref)/np.sqrt(np.sum((focus-ref)**2))
    points = points - ref
    
    # Caculate the point along each line that corresponds to the same z height as points
    d = points[:,2]/norm[0,2]
    xref = d.reshape((-1,1)) * norm

    # extract just the x-y distance between xref and points
    radius = np.sqrt(np.sum((points - xref)**2, axis=1))

    if dynamic:
        mask = 2* radius <= points[:,2]/fnum
    else:
        ztemp = (focus-ref)[0,2]
        mask = 2* radius <= ztemp/fnum

    return mask