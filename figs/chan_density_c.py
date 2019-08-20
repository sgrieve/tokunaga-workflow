import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
import scipy
import numpy as np
from tokunaga_fns import read_toku_data


with open('../data/basin_stats.json') as js:
    basin_data = json.load(js)

with open('../data/ac_data.json') as js:
    ac_data = json.load(js)

threshold = float(sys.argv[1])


c_vals = []
chan_density = []

for toku_id, values in ac_data.items():
    if values[0] > threshold and toku_id in basin_data:
        basin = basin_data[toku_id]

        c_vals.append(values[2])

        _, _, lengths = read_toku_data('../data/TokunagaData_{}.csv'.format(toku_id))

        total_length = np.sum(lengths)

        area = basin[3]
        unchan_area = basin[0]

        chan_density.append(total_length / (area - unchan_area))


# plt.scatter()
plt.hist2d(c_vals, np.log10(chan_density), bins=(50, 50), cmap=plt.cm.viridis, density=False)
plt.show()
