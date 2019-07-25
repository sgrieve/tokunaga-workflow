import matplotlib.pyplot as plt
import json
import tokunaga_fns as toku
from glob import glob
import seaborn as sns
import sys

with open('../data/merged_precip.json') as js:
    precip_data = json.load(js)

file_list = glob('../data/TokunagaData_*_*.csv')

precip_Ntss = []
precip_tss = []
for filename in file_list:

    toku_id = filename.split('TokunagaData_')[1][:-4]

    if toku_id not in precip_data:
        continue

    toku_data, strahler_data, _ = toku.read_toku_data(filename)

    r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)
    threshold = float(sys.argv[1])
    if r_sq > threshold:
        precip_tss.append(precip_data[toku_id])
    else:
        precip_Ntss.append(precip_data[toku_id])


plt.title('Confidence threshold: {}'.format(threshold))

ax = sns.violinplot(data=[precip_tss, precip_Ntss], cut=0, scale='area')
ax.set_xticklabels(['Self-similar', 'Not\nself-similar'])

plt.ylabel('Mean annual precipitation ($mm yr^{-1}$)')

plt.savefig('precip_tss_{}.png'.format(str(threshold).replace('.', '')))
