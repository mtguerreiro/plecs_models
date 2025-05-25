import numpy as np
import scipy.signal

import plecsutil as pu
import py_plecs_models as pm


def params():

    # Plant parameters
    _plant_params = plant_params()

    # Control parameters
    ts = 1e-3
    os = 5

    _casc_params = casc_fbl_get_gains({'ts':ts, 'os':os, 'model':'continuous'})
    _energy_params = energy_get_gains({'ts':ts, 'os':os, 'model':'continuous'})

    ctl_params = {}
    ctl_params.update( _casc_params )
    ctl_params.update( _energy_params )

    # List of controllers
    n_ctl = len(CONTROLLERS)
    active_ctl = 1
    l_ctl = pu.ui.gen_controllers_params(n_ctl, active_ctl)

    # Params for plecs
    _params = {}
    _params.update( _plant_params )
    _params.update( ctl_params )
    _params.update( l_ctl )
    
    return _params


def plant_params():

    V_in = 8
    Vo_ref = 30

    L = 15e-6
    Rl = 15e-3
    
    Co = 100e-6
    R_Co = 25e-3
    Vo_ini = Vo_ref

    R_load = 22

    f_pwm = 100e3
    R_ds = 25e-3

    V_cpl_thres = V_in
    fc_cpl = 10e3
    V_ini_cpl = Vo_ini
    C_cpl = 1e-6

    _params = {}

    _params['V_in'] = V_in
    _params['Vo_ref'] = Vo_ref

    _params['L'] = L
    _params['Rl'] = Rl
    
    _params['Co'] = Co
    _params['R_Co'] = R_Co
    _params['Vo_ini'] = Vo_ini
    
    _params['R_load'] = R_load
    
    _params['f_pwm'] = f_pwm
    _params['R_ds'] = R_ds

    _params['fc_cpl'] = fc_cpl
    _params['V_cpl_thres'] = V_cpl_thres
    _params['V_ini_cpl'] = V_ini_cpl
    _params['C_cpl'] = C_cpl
    
    _params['boost_model'] = 2
    _params['boost_load_model'] = 2
    
    return _params


def casc_fbl_get_gains(ctl_params):

    _plant_params = plant_params()
    
    t_settling = ctl_params['ts']

    _ctl_params = {}
    _ctl_params['t_settling'] = ctl_params['ts']
    _ctl_params['os'] = ctl_params['os']
    _ctl_params['model'] = ctl_params['model']
    _ctl_params['ts'] = 1 / _plant_params['f_pwm']

    __plant_params = {}
    __plant_params['L'] = _plant_params['L']
    __plant_params['Co'] = _plant_params['Co']

    _params = pm.controllers.boost.casc_fblin_params(
        _ctl_params,
        __plant_params,
        prefix='casc_fbl_ctl_'
        )
    
    return _params


def energy_get_gains(ctl_params):
    
    _plant_params = plant_params()
    
    t_settling = ctl_params['ts']

    _ctl_params = {}
    _ctl_params['t_settling'] = ctl_params['ts']
    _ctl_params['os'] = ctl_params['os']
    _ctl_params['model'] = ctl_params['model']
    _ctl_params['ts'] = 1 / _plant_params['f_pwm']

    __plant_params = {}
    __plant_params['L'] = _plant_params['L']
    __plant_params['Co'] = _plant_params['Co']

    _params = pm.controllers.boost.energy_params(
        _ctl_params,
        __plant_params,
        prefix='energy_ctl_'
        )
        
    return _params


CONTROLLERS = {
    'casc_fbl': pu.ui.Controller(port=1, get_gains=casc_fbl_get_gains, label='Cascaded fb lin'),
    'energy' : pu.ui.Controller(port=2, get_gains=energy_get_gains, label='Energy')
}
