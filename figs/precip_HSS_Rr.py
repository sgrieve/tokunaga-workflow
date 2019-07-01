import matplotlib.pyplot as plt
import json
import tokunaga_fns as toku
from glob import glob
import seaborn as sns

with open('../data/merged_precip.json') as js:
    precip_data = json.load(js)

file_list = glob('../data/TokunagaData_*_*.csv')

precip_Nhss = []
precip_hss = []
for filename in file_list:

    toku_id = filename.split('TokunagaData_')[1][:-4]

    if toku_id not in precip_data:
        continue

    _, strahler_data, lengths = toku.read_toku_data(filename)

    Rr_mean, Rr_std = toku.calc_Rr(strahler_data, lengths)

    # 0.67 mean of distribution of std
    # 2.17 mean of distribution of means
    if Rr_mean > 1.5 and Rr_mean < 2.84:
        precip_hss.append(precip_data[toku_id])
    else:
        precip_Nhss.append(precip_data[toku_id])

ax = sns.violinplot(data=[precip_hss, precip_Nhss], cut=0, scale='area')
ax.set_xticklabels(['Self-similar', 'Not\nself-similar'])
plt.title('Testing $R_r$ self-similarity')
plt.ylabel('Mean annual precipitation ($mm yr^{-1}$)')

plt.savefig('precip_hss_Rr.png')
