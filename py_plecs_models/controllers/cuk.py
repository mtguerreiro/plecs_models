import numpy as np
import scipy.signal
import pyctl
import py_plecs_models as ppm

def energy_params(design_params, plant_params, prefix=''):

    t_settling = design_params['t_settling']
    os = design_params['os']

    model = design_params['model']
    ts = design_params['ts']
    if 'alpha' in design_params:
        alpha = design_params['alpha']
    else:
        alpha = 10

    if model == 'continuous':
        model = 1
    elif model == 'discrete':
        model = 2
    else:
        raise TypeError('`model` should be `continuous` or `discrete`.')

    Li = plant_params['Li']
    Lo = plant_params['Lo']
    Cc = plant_params['Cc']
    Co = plant_params['Co']
    
    ky, k_y_dot, k_ey = pyctl.design.pe.cuk.energy(t_settling, os, alpha=alpha)

    _params = {
        'ky': ky, 'k_y_dot': k_y_dot, 'k_ey': k_ey,
        'model': model, 'ts': ts,
        'Li': Li, 'Lo': Lo, 'Cc': Cc, 'Co': Co
    }

    params = ppm.ppm_utils.add_key_prefix_dict(_params, prefix)
    
    return params
