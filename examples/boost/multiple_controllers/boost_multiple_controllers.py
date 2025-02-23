import os

import plecsutil as pu
import model

import matplotlib.pyplot as plt
plt.ion()

# --- Input ---
plecs_file = 'boost_multiple_controllers'
plecs_file_path = os.path.abspath(os.getcwd())

##ctl_params = [
##    ['casc_fbl', {'ts': 0.8e-3, 'os': 5, 'model':'discrete'}],
##    ['casc_fbl', {'ts': 0.8e-3, 'os': 5, 'model':'continuous'}]
##    ]

ctl_params = [
    ['energy', {'ts': 0.8e-3, 'os': 5, 'model':'discrete'}],
    ['energy', {'ts': 0.8e-3, 'os': 5, 'model':'continuous'}],
    ]

##ctl_params = [
##    ['energy', {'ts': 0.8e-3, 'os': 5, 'model':'discrete'}],
##    ['casc_fbl', {'ts': 0.8e-3, 'os': 5, 'model':'continuous'}],
##    ]

sim_params = [
    {'boost_model':2},
    {'boost_model':1}
    ]

# --- Sim ---
# Plecs model
pm = pu.ui.PlecsModel(
    plecs_file, plecs_file_path,
    model.params(),
    controllers=model.CONTROLLERS
    )

# Runs simulations
data  = []
for sp, cp in zip(sim_params, ctl_params):
    d = pm.sim(sim_params=sp, ctl=cp[0], ctl_params=cp[1], close_sim=False)
    data.append(d)

# --- Results ---
plt.figure()
#xlim = [0, 20]

ax = plt.subplot(3,1,1)
plt.title('Duty-cycle')
for d in data:
    label = '{:}'.format( d.meta['ctl_label'] )
    plt.plot(d.t / 1e-3, d.data[:, 3], label=label)
plt.grid()
plt.ylabel('$u$')
plt.legend()
plt.gca().tick_params(labelbottom=False)

plt.subplot(3,1,2, sharex=ax)
plt.title('Inductor current')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 0])
plt.grid()
plt.ylabel('Current (A)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(3,1,3, sharex=ax)
plt.title('Output voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 1])
plt.grid()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
#plt.xlim(xlim)

plt.tight_layout()
