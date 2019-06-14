import matplotlib.pyplot as plt
import seaborn as sns
import tokunaga_fns as toku
import numpy as np
from glob import glob



# Load our data, into lists of filenames catgorized by climate zone

arid = glob('/Users/stuart/toku_data/hpc/TokunagaData_[4-7]_*.csv')
tropical = glob('/Users/stuart/toku_data/hpc/TokunagaData_[1-3]_*.csv')
temperate = glob('/Users/stuart/toku_data/hpc/TokunagaData_8_*.csv')
temperate += glob('/Users/stuart/toku_data/hpc/TokunagaData_11_*.csv')
temperate += glob('/Users/stuart/toku_data/hpc/TokunagaData_14_*.csv')
cold = glob('/Users/stuart/toku_data/hpc/TokunagaData_17_*.csv')
cold += glob('/Users/stuart/toku_data/hpc/TokunagaData_21_*.csv')
cold += glob('/Users/stuart/toku_data/hpc/TokunagaData_25_*.csv')

labels = ['Arid', 'Tropical', 'Temperate', 'Cold']

for i, data in enumerate([arid, tropical, temperate, cold]):
    Cs = []
    for filename in data:

        toku_data, strahler_data = toku.read_toku_data(filename)

        r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)
        threshold = 0.9
        if r_sq > threshold:
            Cs.append(c)

    avg = round(np.mean(Cs), 2)
    std = round(np.std(Cs), 2)
    pc_tss = int(round((len(Cs) / len(data)) * 100, 0))

    sns.distplot(Cs, hist=False, kde=True,
                 kde_kws={'linewidth': 3, 'shade': True},
                 label='{} mean: {} std: {} \nn: {} %TSS: {}'.format(labels[i], avg, std, len(Cs), pc_tss))

plt.title('Confidence threshold: {}'.format(threshold))
plt.xlim(0, 7)
plt.xlabel('c')
plt.ylabel('KDE')
plt.setp(plt.gca().get_legend().get_texts(), fontsize='8')
plt.savefig('koppen_{}_c_dist.png'.format(threshold))
