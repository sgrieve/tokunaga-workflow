import matplotlib.pyplot as plt
import json
import tokunaga_fns as toku
from glob import glob
import sys

with open('../data/merged_precip.json') as js:
    precip_data = json.load(js)

file_list = glob('../data/TokunagaData_*_*.csv')

threshold = float(sys.argv[1])

Cs = []
precip = []
for filename in file_list:

    toku_id = filename.split('TokunagaData_')[1][:-4]

    if toku_id not in precip_data:
        continue

    toku_data, strahler_data, _ = toku.read_toku_data(filename)

    r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)
    if r_sq > threshold:
        Cs.append(c)
        precip.append(precip_data[toku_id])


plt.scatter(Cs, precip, s=25, alpha=0.4, c='k', linewidth=0)

plt.title('Confidence threshold: {}'.format(threshold))
plt.xlim(0, 7)
plt.xlabel('c')
plt.ylabel('Mean annual precipitation ($mm yr^{-1}$)')

plt.savefig('precip_c_{}.png'.format(str(threshold).replace('.', '')))
