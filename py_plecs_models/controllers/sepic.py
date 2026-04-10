import numpy as np
import py_plecs_models as ppm
import pyctl

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

    Li = plant_params['Li']
    Co = plant_params['Co']

    k_ei, kv, k_ev = pyctl.design.pe.sepic.casc_fblin(
        t_settling, os, Li, Co, alpha=alpha
        )

    _params = {
        'k_ei': k_ei, 'k_ev': k_ev, 'kv': kv,
        'model': model, 'ts': ts
    }

    params = ppm.ppm_utils.add_key_prefix_dict(_params, prefix)
    
    return params
