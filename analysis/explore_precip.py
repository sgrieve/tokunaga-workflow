import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from glob import glob
import seaborn as sns
import json

def N_i_j(i, j, data):
    count = 0
    ij = int('{}{}'.format(i, j))
    for tok in data:
        if tok == ij:
            count += 1
    return count

def N_i(i, data):
    count = 0
    for tok in data:
        if str(tok).startswith(str(i)):
            count += 1

    return count

def T_i_j(i, j, data):
    top = N_i_j(i, j, toku)
    bottom = N_i(j, toku)

    return top/bottom

def T_k(i, k, data):
    return T_i_j(i, i+k, toku)


def z_k(k, omega, data):
    count = 0
    for i in range(omega - k):
        for l in range(N_i(i + 1, data)):
            count += 1

    return count

def f(k, a, c):
    return a * np.power(c, k - 1)


As_lo = []
Cs_lo = []
As_hi = []
Cs_hi = []

with open('/Users/stuart/tokunaga-workflow/analysis/merged_precip.json') as js:
    precip_data = json.load(js)

file_list = glob('/Users/stuart/toku_data/hpc/TokunagaData_*_*.csv')

for i, filename in enumerate(file_list):
    # print(i, 'of', len(files))

    toku_id = filename.split('TokunagaData_')[1][:-4]

    if toku_id not in precip_data:
        continue

    with open(filename) as f_data:
        f_data.readline()
        data = f_data.readlines()

    toku = []
    strahler = []

    for d in data:
        s = d.split(',')
        strahler.append(int(s[0]))
        toku.append(int(s[1]))

    omega = max(strahler)
    # print(omega, max(toku))

    # if omega < 6:
    #     continue

    x = []
    y = []

    for k in range(1, omega+1):
        # print('k:', k)
        for i in range(1, omega+1):
            # print('i:', i)
            if ((i + k) <= omega) and ((i + k) >= 2):

                tk = T_k(i, k, toku)
                x.append(k)
                y.append(tk)

    # a = T_i_j(1, 1, toku)
    # c = T_k(2, 2, toku) / T_k(2, 1, toku)

    # print('a:', a)
    # print('c:', c)

    n = len(x)

    # model_x = np.linspace(1,4,100)

    weights = [z_k(k, omega, toku) for k in x]

    weights = np.sqrt(weights)
    norm_weights = []

    for w in weights:
        W = (w - np.min(weights)) / (np.max(weights) - np.min(weights))
        norm_weights.append((1 - W) + 0.01)

    p0 = 1.26, 2.4

    popt, pcov = curve_fit(f, x, y, p0, sigma=norm_weights, absolute_sigma=False)
    # model_y = f(model_x, popt[0], popt[1])

    residuals = np.array(y) - f(np.array(x), popt[0], popt[1])
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # print('Weighted fit parameters:', popt, 'R squared:', r_squared)
    if r_squared >= 0.8:
        if precip_data[toku_id] < 1600:
            As_lo.append(popt[0])
            Cs_lo.append(popt[1])
        else:
            As_hi.append(popt[0])
            Cs_hi.append(popt[1])

        # 5938.8516083170425 is the max precip in the dataset
        # marker_size = ((precip_data[toku_id] / 5938.8516083170425) * 150) + 1
        # plt.scatter(popt[0], popt[1], s=marker_size, c='b')

        # plt.ylim(0.1, 10000)
        # plt.xlim(0,11)
        # plt.yscale('log')
        # plt.plot(x, y, '.r')
        # plt.plot(model_x, model_y, 'k--')
        # plt.show()
        # plt.clf()

#
# plt.ylim(1.5, 5)
# plt.xlim(0.6, 1.8)


sns.distplot(Cs_lo, hist=False, kde=True,
             kde_kws={'linewidth': 3, 'shade': True}, label='low')

sns.distplot(Cs_hi, hist=False, kde=True,
             kde_kws={'linewidth': 3, 'shade': True}, label='high')


plt.xlim(0,6)


print('high', np.mean(As_hi), np.mean(Cs_hi), len(Cs_hi))
print('low', np.mean(As_lo), np.mean(Cs_lo), len(Cs_lo))

plt.savefig('precip_data.png')
plt.clf()
