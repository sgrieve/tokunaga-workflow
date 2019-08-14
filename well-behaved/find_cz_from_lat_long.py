import json
import sys
from shapely.geometry import Polygon, Point


def bounds_to_poly(bbox):
    '''
    Helper function to go from lat and long max and min values to a shapely
    polygon
    '''
    return Polygon(((bbox[1], bbox[3]), (bbox[0], bbox[3]),
                   (bbox[0], bbox[2]), (bbox[1], bbox[2])))


with open('../processing/bboxes.json') as f:
    data = json.load(f)

long = float(sys.argv[1])  # 76.668
lat = float(sys.argv[2])  # 31.764

point = Point(lat, long)

for a, b in data.items():

    cz_poly = bounds_to_poly(b['bbox'])
    if cz_poly.contains(point):
        print(a)
        break
