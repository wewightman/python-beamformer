import numpy as np
import pytest

def gen_ref_n_points():
    ref = np.zeros((1, 3))
    points = np.array(
        [[0, 0, 0],
        [1, 1, 0],
        [-1, -1, 0],
        [0, 0, 1]]
    )
    return {'ref':ref, 'points':points}

def gen_bmfrm():
    from bmfrm import Beamformer
    bmfrm = Beamformer()
    bmfrm.c = 2
    return bmfrm

def test_rxengine_values():
    from bmfrm.trigengines import rxengine
    dist = rxengine(gen_bmfrm(), **gen_ref_n_points())
    dist_known = np.array([0, np.sqrt(2)/2, np.sqrt(2)/2, 0.5])
    assert dist == pytest.approx(dist_known)

def test_rxengine_length():
    from bmfrm.trigengines import rxengine
    dist = rxengine(gen_bmfrm(), **gen_ref_n_points())
    assert len(dist.shape) == 1 and dist.shape[0] == 4

