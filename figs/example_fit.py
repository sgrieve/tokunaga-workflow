import matplotlib.pyplot as plt
import seaborn as sns
import tokunaga_fns as toku
import numpy as np
from glob import glob

filename = '../data/TokunagaData_25_44_45dab36e_67d9_4ba0_a243_a73ed6b6ed11_0.csv'

toku_data, strahler_data = toku.read_toku_data(filename)

r_sq, a, c, x, y = toku.fit_a_and_c_x_y(toku_data, strahler_data)

model_x = np.linspace(1,6,100)
model_y = toku.f(model_x, a, c)

annotation1 = '$T_{k} = a c^{k-1}$'
annotation2 = '$a = ' + str(round(a, 2)) + '$ $c = ' + str(round(c, 2)) + '$'
annotation3 = '$R^2 = ' + str(round(r_sq, 2)) + '$'

plt.text(0.5, 40, annotation1, fontsize='18')
plt.text(0.5, 20, annotation2, fontsize='12')
plt.text(0.5, 12.5, annotation3, fontsize='12')

plt.ylim(0.5, 100)
plt.xlim(0, 7)
plt.yscale('log')
plt.plot(x, y, '.b')
plt.plot(model_x, model_y, 'k--')
plt.xlabel('$k$')
plt.ylabel('$T_k$')
plt.savefig('fit_example.png')
