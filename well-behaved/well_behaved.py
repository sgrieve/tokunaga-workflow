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

threshold = float(sys.argv[1])

# High DD
hi_data = glob('../data/TokunagaData_11_30_2b66179e_550c_41f3_854c_05ea5e7363ef*')
hi_data += glob('../data/TokunagaData_25_44_09964bd1_d3f8_4cea_bede_3a5ad3e44993*')
hi_data += glob('../data/TokunagaData_25_44_a7447966_3d7f_4b4c_8b6e_a039b0be0db6*')
hi_data += glob('../data/TokunagaData_17_36*')
hi_data += glob('../data/TokunagaData_8_48_0ff8f623_07bb_4649_ae7a_3016549f3783*')

# low DD
lo_data = glob('../data/TokunagaData_25_44_b4a0607f_a5d6_4723_8533_7e6e67c474dc*')
lo_data += glob('../data/TokunagaData_25_44_a567493c_b18d_49e5_8b75_c4a112618ec3*')
lo_data += glob('../data/TokunagaData_7_86*')
lo_data += glob('../data/TokunagaData_14_174_ddc1c40e_c8f1_4732_811b_2c6e1212e9cd*')
lo_data += glob('../data/TokunagaData_6_11_89c88345_9e49_460b_ae18_d7fec5cad053*')

for i, data in enumerate([hi_data, lo_data]):
    Cs = []
    for filename in data:

        toku_data, strahler_data, _ = toku.read_toku_data(filename)

        r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)

        if r_sq > threshold:
            Cs.append(c)

    avg = round(np.mean(Cs), 2)
    std = round(np.std(Cs), 2)
    pc_tss = int(round((len(Cs) / len(data)) * 100, 0))

    # print(Cs)

    plt.scatter(np.ones(len(Cs)) + i, Cs)
plt.show()
