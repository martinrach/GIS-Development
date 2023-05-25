
#test file to select right point cloud from a set of point clouds

import laspy
from shapely import Point, Polygon
import geopandas as gpd
import Visualize_data
import numpy as np

x = 377000
y = 6678000
x_end =  380000
y_end =  6675000
coords = (((x, y), (x_end, y), (x_end, y_end), (x, y_end)))
polygon = Polygon(coords)
area = gpd.GeoSeries(polygon)
bbox = gpd.GeoDataFrame({'geometry': area})
bbox = bbox.set_crs(3067, allow_override=True)

with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS-project/Input data/L4131G3.laz_classified.las") as temp:
    print(temp)
    input_las = temp.read()
    print(input_las)
    print('Points from data:', len(input_las.points))

print(input_las.X, input_las.Y)
point_format = input_las.point_format
point_data = np.stack([input_las.X, input_las.Y, input_las.Z], axis=0).transpose((1, 0))
print(point_data)

Visualize_data.visualize_data(point_data)
