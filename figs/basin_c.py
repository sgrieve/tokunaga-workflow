import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
import scipy
import numpy as np
from math import radians


with open('../data/basin_stats.json') as js:
    basin_data = json.load(js)

with open('../data/ac_data.json') as js:
    ac_data = json.load(js)

threshold = float(sys.argv[1])


labels = ['Slope', 'Area', 'Relief', 'Relief_over_Area']

for i in range(4):

    x, y = [], []

    for toku_id, values in ac_data.items():
        if values[0] > threshold and toku_id in basin_data:
            basin = basin_data[toku_id]

            x.append(values[2])

            if i == 0:
                y.append(basin[1])
            elif i == 1:
                y.append(basin[3])
            elif i == 2:
                y.append(basin[4] - basin[5])
            elif i == 3:
                y.append((basin[4] - basin[5]) / basin[3])

    # if i == 1 or i == 3:
    #     plt.yscale('log')

    # plt.scatter(x, y)
    plt.hist2d(x, np.log10(y), bins=(50, 50), cmap=plt.cm.viridis, density=False)

    plt.ylabel(labels[i])
    plt.xlabel('c')
    plt.tight_layout()
    plt.savefig('{}.png'.format(labels[i]))
    plt.clf()


c_vals, aspect = [], []

for toku_id, values in ac_data.items():
    if values[0] > threshold and toku_id in basin_data:
        basin = basin_data[toku_id]

        c_vals.append(values[2])
        aspect.append(radians(basin[2]))

ax = plt.subplot(111, polar=True)
ax.scatter(x=aspect, y=c_vals)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

plt.savefig('aspect.png')
