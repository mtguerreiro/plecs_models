import numpy as np
import scipy.signal


def casc_fblin_params(design_params, plant_params, prefix=''):

    t_settling = design_params['t_settling']
    os = design_params['os']

    model = design_params['model']
    ts = design_params['ts']

    if model == 'continuous':
        model = 1
    elif model == 'discrete':
        model = 2
    else:
        raise TypeError('`model` should be `continuous` or `discrete`.')

    L = plant_params['L']
    C = plant_params['C_out']

    zeta_i, wn_i = _zeta_wn(t_settling / 5, os)
    k_ei = - L * wn_i**2
    ki  =   2 * L * zeta_i * wn_i

    zeta_v, wn_v = _zeta_wn(t_settling, os)
    k_ev = - C * wn_v**2
    kv  =   2 * C * zeta_v * wn_v

    _params = {
        'k_ei': k_ei, 'ki': ki, 'k_ev': k_ev, 'kv': kv,
        'model': model, 'ts': ts
    }

    params = _add_key_prefix_dict(_params, prefix)
    
    return params


def energy_params(design_params, plant_params, prefix=''):

    t_settling = design_params['t_settling']
    os = design_params['os']

    model = design_params['model']
    ts = design_params['ts']

    if model == 'continuous':
        model = 1
    elif model == 'discrete':
        model = 2
    else:
        raise TypeError('`model` should be `continuous` or `discrete`.')

    L = plant_params['L']
    C_out = plant_params['C_out']
    
    zeta, wn = _zeta_wn(t_settling, os)

    A = np.array([[ 0.0, 1.0, 0.0],
                  [ 0.0, 0.0, 0.0],
                  [-1.0, 0.0, 0.0]])

    B = np.array([[0.0], [1.0], [0.0]])
    
    p1 = -zeta * wn + 1j * wn * np.sqrt(1 - zeta**2)
    p2 = np.conj(p1)
    p3 = 5 * p1.real

    poles = [p1, p2, p3]

    K = scipy.signal.place_poles(A, B, poles).gain_matrix.reshape(-1)

    _params = {
        'ky': K[0], 'k_y_dot': K[1], 'k_ey': K[2],
        'model': model, 'ts': ts,
        'L': L, 'C_out': C_out
    }

    params = _add_key_prefix_dict(_params, prefix)
    
    return params


def _add_key_prefix_dict(_dict, prefix):

    new_dict = {}
    for key, val in _dict.items():
        new_dict[f"{prefix}{key}"] = val

    return new_dict


def _zeta_wn(ts, os):

    zeta = -np.log(os / 100) / np.sqrt( np.pi**2 + np.log(os / 100)**2 )
    wn = 4 / ts / zeta

    return (zeta, wn)
