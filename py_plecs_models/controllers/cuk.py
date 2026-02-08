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

    Li = plant_params['Li']
    Co = plant_params['Co']

    k_ei, kv, k_ev = pyctl.design.pe.cuk.casc_fblin(
        t_settling, os, Li, Co, alpha=alpha
        )

    _params = {
        'k_ei': k_ei, 'k_ev': k_ev, 'kv': kv,
        'model': model, 'ts': ts
    }

    params = ppm.ppm_utils.add_key_prefix_dict(_params, prefix)
    
    return params


def lin_sfb_params(design_params, plant_params, prefix=''):

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

    L1 = plant_params['Li']
    L2 = plant_params['Lo']
    Cc = plant_params['Cc']
    Co = plant_params['Co']
    v_in = plant_params['V_in']
    vo = plant_params['Vo_ref']
    po = plant_params['Po_nom']
    nt = plant_params['nt']
    
    K, x1_ss, x2_ss, x3_ss, x4_ss, u_ss = pyctl.design.pe.iso_cuk.lin_state_feedback(
        t_settling, os,
        L1, L2, Cc, Co, v_in, vo, po, nt, alpha
        )

    _params = {
        'K': K,
        'x1_ss': x1_ss, 'x2_ss': x2_ss, 'x3_ss': x3_ss, 'x4_ss': x4_ss,
        'u_ss': u_ss,
        'model': model, 'ts': ts,
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
