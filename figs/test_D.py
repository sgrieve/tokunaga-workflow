import tokunaga_fns as toku
from glob import glob
import numpy as np

file_list = glob('../data/TokunagaData_*_*.csv')

Ds = []
for filename in file_list:

    _, strahler_data, lengths = toku.read_toku_data(filename)

    Rr_mean, Rr_std = toku.calc_Rr(strahler_data, lengths)
    Rb_mean, Rb_std = toku.calc_Rb(strahler_data)

    D = toku.D(Rb_mean, Rr_mean)
    if Rr_mean < 1.05:
        continue

    Ds.append(D)

print('Mean: {} StdDev: {}'.format(np.mean(Ds), np.std(Ds)))
