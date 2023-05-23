
#test file to select right point cloud from a set of point clouds

import laspy
from shapely import Point, Polygon
import geopandas as gpd

x = 377000
y = 6678000
x_end =  380000
y_end =  6675000
coords = (((x, y), (x_end, y), (x_end, y_end), (x, y_end)))
polygon = Polygon(coords)
area = gpd.GeoSeries(polygon)
bbox = gpd.GeoDataFrame({'geometry': area})
bbox = bbox.set_crs(3067, allow_override=True)

with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS-project/Input data/Pointcloud/leppävaara.laz") as temp:
    print(temp)
    input_las = temp.read()
    print(input_las)
    print('Points from data:', len(input_las.points))

print(input_las.X, input_las.Y)
point_format = input_las.point_format

print(point_format.id)

print(list(point_format.dimension_names))

print(input_las.xyz)
points = input_las.xyz
point = points[0]
print(point)
p = Point(point[0], point[1])
point_xy = gpd.GeoSeries(p)
point1 = gpd.GeoDataFrame({'geometry': point_xy})
point1 = point1.set_crs(3067, allow_override=True)

overlay = gpd.overlay(point1, bbox, how='intersection')
print(overlay)
if overlay is not None:
    print("Success!")