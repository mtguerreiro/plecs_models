import os

import plecsutil as pu
import model

import matplotlib.pyplot as plt
plt.ion()

# --- Input ---
plecs_file = 'cuk_model'
plecs_file_path = os.path.abspath(os.getcwd())

sim_params = [
    [{'cuk_model':2}, {'ts':2.5e-3, 'os':5, 'model':'discrete'}],
    [{'cuk_model':1}, {'ts':2.5e-3, 'os':5, 'model':'continuous'}],
    ]

# --- Sim ---
# Plecs model
pm = pu.ui.PlecsModel(
    plecs_file, plecs_file_path,
    model.params(),
    get_ctl_gains = model.energy_get_gains
    )

# Runs simulations
data  = []
for sp in sim_params:
    d = pm.sim(sim_params=sp[0], ctl_params=sp[1], close_sim=False)
    data.append(d)
    
# --- Results ---
plt.figure(figsize=(7,9))

ax = plt.subplot(6,1,1)
plt.title('Duty-cycle')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 6])
plt.grid()
plt.ylabel('Duty-cycle')
plt.gca().tick_params(labelbottom=False)

plt.subplot(6,1,2, sharex=ax)
plt.title('Input inductor current')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 0])
plt.grid()
plt.ylabel('Current (A)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(6,1,3, sharex=ax)
plt.title('Output inductor current')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 1])
plt.grid()
plt.ylabel('Current (A)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(6,1,4, sharex=ax)
plt.title('Prim. side coupling cap. voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 3])
plt.grid()
plt.ylabel('Voltage (V)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(6,1,5, sharex=ax)
plt.title('Sec. side coupling cap. voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 4])
plt.grid()
plt.ylabel('Voltage (V)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(6,1,6, sharex=ax)
plt.title('Output voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 5])
plt.plot(data[0].t / 1e-3, data[0].data[:, 7], '--k')
plt.grid()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
#plt.xlim(xlim)

plt.tight_layout()
