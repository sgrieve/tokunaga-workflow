import matplotlib.pyplot as plt
import seaborn as sns
import tokunaga_fns as toku
import numpy as np
from glob import glob
import sys

# Load our data, into lists of filenames catgorized by climate zone

arid = glob('../data/TokunagaData_[4-7]_*.csv')
tropical = glob('../data/TokunagaData_[1-3]_*.csv')
temperate = glob('../data/TokunagaData_8_*.csv')
temperate += glob('../data/TokunagaData_11_*.csv')
temperate += glob('../data/TokunagaData_14_*.csv')
cold = glob('../data/TokunagaData_17_*.csv')
cold += glob('../data/TokunagaData_21_*.csv')
cold += glob('../data/TokunagaData_25_*.csv')

labels = ['Arid', 'Tropical', 'Temperate', 'Cold']
colours = ['r', 'g', 'k', 'b']

threshold = float(sys.argv[1])

for i, data in enumerate([arid, tropical, temperate, cold]):
    Cs = []
    As = []
    for filename in data:

        toku_data, strahler_data, _ = toku.read_toku_data(filename)

        r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)

        if r_sq > threshold:
            Cs.append(c)
            As.append(a)

    plt.scatter(As, Cs, s=25, alpha=0.2, c=colours[i], linewidth=0,
                label=labels[i])

plt.title('Confidence threshold: {}'.format(threshold))
plt.ylim(0, 7)
plt.ylabel('c')
plt.xlabel('a')
plt.legend()
plt.savefig('koppen_{}_a_c.png'.format(str(threshold).replace('.', '')))
