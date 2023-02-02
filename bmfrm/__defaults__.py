import numpy as np

pwdefaults = []
txparams = {}
parametric = {}
parametric['keys'] = ['steer', 'focus']
txparams['mode'] = {'parametric':parametric}

# expected default modes
alinedefaults = []
__txparams__ = {}
__parametric__ = {}
__parametric__['keys'] = ['steer', 'focus']
__txparams__['mode'] = {'parametric' : __parametric__}
alinedefaults['txparams'] = __txparams__