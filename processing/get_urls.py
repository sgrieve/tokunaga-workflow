import json
import sys

with open('/data/home/faw513/tokunaga-workflow/processing/download_links.json') as srtm:
    links = json.load(srtm)

for url in links[sys.argv[1]]:
    print(url)
