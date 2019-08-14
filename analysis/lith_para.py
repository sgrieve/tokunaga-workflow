from shapely.geometry import Point, MultiPoint, mapping, MultiLineString
import fiona
import csv
from rasterstats import zonal_stats
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import math
import json
from glob import glob
import sys

def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.

    From http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/

    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull

    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])

    coords = np.array([point.coords[0]
                       for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        if area == 0:
            continue
        circum_r = a*b*c/(4.0*area)
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = MultiLineString(edge_points)
    triangles = list(polygonize(m))

    return cascaded_union(triangles), edge_points

liths = {}

filename = sys.argv[1]
points = []

with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in reader:
        points.append(Point(float(row[1]), float(row[0])))

concave_hull, _ = alpha_shape(MultiPoint(points[::25]), alpha=10.5)
stats = zonal_stats(concave_hull, '/data/Geog-c2s2/glim.tif', stats="majority")

toku_id = filename.split('toku_network_')[1][:-4]
liths[toku_id] = stats[0]['majority']

with open('/data/Geog-c2s2/toku/toku-data-{}.json'.format(toku_id), 'w') as outfile:
    json.dump(liths, outfile)

print('Success')
