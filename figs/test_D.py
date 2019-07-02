import tokunaga_fns as toku
from glob import glob
import numpy as np

arid = glob('../data/TokunagaData_[4-7]_*.csv')
tropical = glob('../data/TokunagaData_[1-3]_*.csv')
temperate = glob('../data/TokunagaData_8_*.csv')
temperate += glob('../data/TokunagaData_11_*.csv')
temperate += glob('../data/TokunagaData_14_*.csv')
cold = glob('../data/TokunagaData_17_*.csv')
cold += glob('../data/TokunagaData_21_*.csv')
cold += glob('../data/TokunagaData_25_*.csv')

labels = ['Arid', 'Tropical', 'Temperate', 'Cold']
All_Data = []

for i, data in enumerate([arid, tropical, temperate, cold]):
    Ds = []
    for filename in data:

        _, strahler_data, lengths = toku.read_toku_data(filename)

        Rr_mean, Rr_std = toku.calc_Rr(strahler_data, lengths)
        Rb_mean, Rb_std = toku.calc_Rb(strahler_data)

        if Rr_mean < 1.05:
            continue

        D = toku.D(Rb_mean, Rr_mean)
        Ds.append(D)
        All_Data.append(D)

    print('{} Mean: {} StdDev: {}'.format(labels[i], np.mean(Ds), np.std(Ds)))
print('All Data Mean: {} StdDev: {}'.format(np.mean(All_Data), np.std(All_Data)))
