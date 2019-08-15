import tokunaga_fns as toku
from glob import glob
import json
import sys

# Load our data, into lists of filenames catgorized by climate zone
data = glob('/data/Geog-c2s2/toku/*/TokunagaData_*.csv')

# Make sure no wierd filesystem stuff messes up the order of the file list we are slicing
data.sort()

data_dict = {}

start = int(sys.argv[1])
end = int(sys.argv[2])

for filename in data[start:end]:
    toku_id = filename.split('TokunagaData_')[1][:-4]
    toku_data, strahler_data, _ = toku.read_toku_data(filename)

    r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)

    data_dict[toku_id] = [r_sq, a, c]

with open('/data/Geog-c2s2/a_c_data/a_c_data_{}_{}.json'.format(start, end), 'w') as fp:
    json.dump(data_dict, fp)

print('Done')
