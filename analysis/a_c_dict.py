import tokunaga_fns as toku
from glob import glob
import json

# Load our data, into lists of filenames catgorized by climate zone
data = glob('../data/TokunagaData_*.csv')

data_dict = {}

for filename in data:
    toku_id = filename.split('TokunagaData_')[1][:-4]
    toku_data, strahler_data, _ = toku.read_toku_data(filename)

    r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)

    data_dict[toku_id] = [r_sq, a, c]

with open('a_c_data.json', 'w') as fp:
    json.dump(data_dict, fp)
