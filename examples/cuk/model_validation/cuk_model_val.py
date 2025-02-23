import os

import plecsutil as pu
import model

import matplotlib.pyplot as plt
plt.ion()

# --- Input ---
plecs_file = 'cuk_model_val'
plecs_file_path = os.path.abspath(os.getcwd())

sim_params = [
    {'cuk_model':1},
    {'cuk_model':2}
    ]

# --- Sim ---
# Plecs model
pm = pu.ui.PlecsModel(
    plecs_file, plecs_file_path,
    model.params(),
    )

# Runs simulations
data  = []
for sp in sim_params:
    d = pm.sim(sim_params=sp, close_sim=False)
    data.append(d)
    
# --- Results ---
plt.figure(figsize=(7,8))


ax = plt.subplot(5,1,1)
plt.title('Input inductor current')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 0])
plt.grid()
plt.ylabel('Current (A)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(5,1,2, sharex=ax)
plt.title('Output inductor current')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 1])
plt.grid()
plt.ylabel('Current (A)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(5,1,3, sharex=ax)
plt.title('Prim. side coupling cap. voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 3])
plt.grid()
plt.ylabel('Voltage (V)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(5,1,4, sharex=ax)
plt.title('Sec. side coupling cap. voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 4])
plt.grid()
plt.ylabel('Voltage (V)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(5,1,5, sharex=ax)
plt.title('Output voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 5])
plt.grid()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
#plt.xlim(xlim)

plt.tight_layout()
