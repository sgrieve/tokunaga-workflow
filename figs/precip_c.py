import matplotlib.pyplot as plt
import json
import tokunaga_fns as toku
from glob import glob

with open('/Users/stuart/tokunaga-workflow/analysis/merged_precip.json') as js:
    precip_data = json.load(js)

file_list = glob('/Users/stuart/toku_data/hpc/TokunagaData_*_*.csv')

Cs = []
precip = []
for filename in file_list:

    toku_id = filename.split('TokunagaData_')[1][:-4]

    if toku_id not in precip_data:
        continue

    toku_data, strahler_data = toku.read_toku_data(filename)

    r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)
    threshold = 0.8
    if r_sq > threshold:
        Cs.append(c)
        precip.append(precip_data[toku_id])


plt.scatter(Cs, precip, s=25, alpha=0.4, c='k', linewidth=0)

plt.title('Confidence threshold: {}'.format(threshold))
plt.xlim(0, 7)
plt.xlabel('c')
plt.ylabel('Mean annual precipitation ($mm yr^{-1}$)')

plt.savefig('precip_c_{}.png'.format(threshold))
