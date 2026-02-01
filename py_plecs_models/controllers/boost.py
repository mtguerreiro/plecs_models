import numpy as np
import scipy.signal
import pyctl
import py_plecs_models as ppm


def casc_fblin_params(design_params, plant_params, prefix=''):

    t_settling = design_params['t_settling']
    os = design_params['os']
    if 'alpha' in design_params:
        alpha = design_params['alpha']
    else:
        alpha = 10

    model = design_params['model']
    ts = design_params['ts']

    if model == 'continuous':
        model = 1
    elif model == 'discrete':
        model = 2
    else:
        raise TypeError('`model` should be `continuous` or `discrete`.')

    L = plant_params['L']
    C = plant_params['Co']

    k_ei, kv, k_ev = pyctl.design.pe.boost.casc_fblin(
        t_settling, os, L, C, alpha=alpha
        )

    _params = {
        'k_ei': k_ei, 'k_ev': k_ev, 'kv': kv,
        'model': model, 'ts': ts
    }

    params = ppm.ppm_utils.add_key_prefix_dict(_params, prefix)
    
    return params


def energy_params(design_params, plant_params, prefix=''):

    t_settling = design_params['t_settling']
    os = design_params['os']

    model = design_params['model']
    ts = design_params['ts']

    if 'alpha' in design_params:
        alpha = design_params['alpha']
    else:
        alpha = 5
        
    if model == 'continuous':
        model = 1
    elif model == 'discrete':
        model = 2
    else:
        raise TypeError('`model` should be `continuous` or `discrete`.')

    L = plant_params['L']
    Co = plant_params['Co']
    
    ky, k_y_dot, k_ey = pyctl.design.pe.boost.energy(t_settling, os, alpha=alpha)

    _params = {
        'ky': ky, 'k_y_dot': k_y_dot, 'k_ey': k_ey,
        'model': model, 'ts': ts,
        'L': L, 'Co': Co
    }

    params = ppm.ppm_utils.add_key_prefix_dict(_params, prefix)
    
    return params
