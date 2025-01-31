
class VirtualSyncBoost:

    def __init__(self):

        self.params = {
            'BOOST_MODEL': 1,
            'L': 15e-6,
            'C_out': 100e-6,
            'V_out_init': 15,
            
            'RL': 15e-3,
            'R_C_out': 20e-3,
            'f_pwm': 100e3,
            'R_ds': 20e-3,

            'BOOST_LOAD_MODEL': 1,
            'R_load': 22,
            'v_thres': 10,
            'fc_cpl': 1e3,
        }
