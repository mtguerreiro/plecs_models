import numpy as np
import scipy.signal


class CascFblin:

    def __init__(self):
    
        pass        


    def get_params(self, design_params, plant_params):

        ts = design_params['ts']
        os = design_params['os']

        model = design_params['model']
        t_sampling = ['t_sampling']

        if model == 'continuous':
            model = 1
        else:
            model = 2

        L = plant_params['L']
        C = plant_params['C_out']

        zeta_i, wn_i = _zeta_wn(ts / 5, os)
        k_ei = - L * wn_i**2
        ki  =   2 * L * zeta_i * wn_i

        zeta_v, wn_v = _zeta_wn(ts, os)    
        k_ev = - C * wn_v**2
        kv  =   2 * C * zeta_v * wn_v

        params = {
            'k_ei': k_ei, 'ki': ki, 'k_ev': k_ev, 'kv': kv,
            'CASC_FBLIN_CONTROL_MODEL': model,
            
        }
        
        return params


def _zeta_wn(ts, os):

    zeta = -np.log(os / 100) / np.sqrt( np.pi**2 + np.log(os / 100)**2 )
    wn = 4 / ts / zeta

    return (zeta, wn)
