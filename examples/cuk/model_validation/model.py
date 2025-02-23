import numpy as np
import scipy.signal

import plecsutil as pu
import py_plecs_models as pm


def params():

    # Plant parameters
    _plant_params = plant_params()

    # Params for plecs
    _params = {}
    _params.update( _plant_params )
    
    return _params


def plant_params():

    V_in = 25
    Vo_ref = 30

    Li = 100e-6
    R_Li = 0 # 40e-3

    Lo = 150e-6
    R_Lo = 0 # 10e-3
    
    C1 = 9.4e-6
    R_C1 = 0 # 2.5e-3
    V1_ini = V_in

    C2 = C1
    R_C2 = R_C1
    V2_ini = Vo_ref

    Co = 330e-6
    R_Co = 0 # 60e-3
    Vo_ini = Vo_ref
    
    f_pwm = 100e3
    R_ds = 0 # 25e-3

    R_load = 22

    nt = 5/3
    
    V_cpl_thres = 15
    fc_cpl = 100e3

    _params = {}

    _params['V_in'] = V_in
    _params['Vo_ref'] = Vo_ref

    _params['Li'] = Li
    _params['R_Li'] = R_Li

    _params['Lo'] = Lo
    _params['R_Lo'] = R_Lo

    _params['C1'] = C1
    _params['R_C1'] = R_C1
    _params['V1_ini'] = V1_ini

    _params['C2'] = C2
    _params['R_C2'] = R_C2
    _params['V2_ini'] = V2_ini
    
    _params['Co'] = Co
    _params['R_Co'] = R_Co
    _params['Vo_ini'] = Vo_ini

    _params['nt'] = nt
    
    _params['R_load'] = R_load
    
    _params['f_pwm'] = f_pwm
    _params['R_ds'] = R_ds

    _params['fc_cpl'] = fc_cpl
    _params['V_cpl_thres'] = V_cpl_thres
    
    _params['cuk_model'] = 1
    _params['cuk_load_model'] = 1
    
    return _params
