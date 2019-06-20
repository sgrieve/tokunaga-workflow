import json
from glob import glob

files = glob('../jsons/*.json')

joined_data = {}

for f in files:
    with open(f) as js:
        data = json.load(js)

    joined_data.update(data)

with open('merged_precip.json', 'w') as outfile:
    json.dump(joined_data, outfile)
