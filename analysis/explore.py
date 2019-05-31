import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from glob import glob
import seaborn as sns

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


arid = glob('/Users/stuart/toku_data/hpc/TokunagaData_[4-7]_*.csv')
tropical = glob('/Users/stuart/toku_data/hpc/TokunagaData_[1-3]_*.csv')
temperate = glob('/Users/stuart/toku_data/hpc/TokunagaData_8_*.csv')
temperate += glob('/Users/stuart/toku_data/hpc/TokunagaData_11_*.csv')
temperate += glob('/Users/stuart/toku_data/hpc/TokunagaData_14_*.csv')
cold = glob('/Users/stuart/toku_data/hpc/TokunagaData_17_*.csv')
cold += glob('/Users/stuart/toku_data/hpc/TokunagaData_21_*.csv')
cold += glob('/Users/stuart/toku_data/hpc/TokunagaData_25_*.csv')

labels = ['Arid', 'Tropical', 'Temperate', 'Cold']

for q, files in enumerate([arid, tropical, temperate, cold]):

    As = []
    Cs = []

    reject_count = 0
    total_count = 0
    for i, filename in enumerate(files):
        # print(i, 'of', len(files))

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

        # if omega < 5:
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
            As.append(popt[0])
            Cs.append(popt[1])
        else:
            reject_count += 1

        total_count += 1

            # plt.ylim(0.1, 10000)
            # plt.xlim(0,11)
            # plt.yscale('log')
            # plt.plot(x, y, '.r')
            # plt.plot(model_x, model_y, 'k--')
            # plt.show()
            # plt.clf()


    # plt.ylim(1.5, 5)
    # plt.xlim(0.6, 1.8)
    # plt.plot(As, Cs, 'k.')
    print(np.mean(As), np.mean(Cs), len(Cs))

    avg = round(np.mean(Cs), 2)
    std = round(np.std(Cs), 2)

    print(labels[q], reject_count/total_count)

    sns.distplot(Cs, hist=False, kde=True,
                 kde_kws={'linewidth': 3, 'shade': True}, label='{} c: {} std: {}'.format(labels[q], avg, std))


# plt.hist(Cs, bins=50)
plt.xlim(0,6)

plt.savefig('full_data_kde.png')
plt.clf()
