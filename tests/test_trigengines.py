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

def test_rxengine_values():
    from bmfrm.trigengines import rxengine
    c = 2
    tau = rxengine(c, **gen_ref_n_points())
    tau_known = np.array([0, np.sqrt(2)/c, np.sqrt(2)/c, 1/c])
    assert tau == pytest.approx(tau_known)

def test_rxengine_length():
    from bmfrm.trigengines import rxengine
    c = 2
    tau = rxengine(c, **gen_ref_n_points())
    assert np.ndim(tau) == 1 and tau.shape[0] == 4

def test_pwtxengine_values():
    from bmfrm.trigengines import pwtxengine
    c = 2
    tref = 0.5
    theta = 0
    phi = 0
    tau = pwtxengine(c, tref, theta, phi, **gen_ref_n_points())
    tau_known = np.array([1, 1, 1, 2])/c
    assert tau == pytest.approx(tau_known)