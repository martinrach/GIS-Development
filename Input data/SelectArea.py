from shapely.geometry import Polygon, Point
import rasterio
import geopandas as gpd
import laspy

#Give coordinates in planar coordinates in TM35FIN. Areas inside polygon will be included into calculations

#check whether each tile overlaps the defined polygon.
#   with dems check the transform parameter after opening it and x = transform[2] and y = transform[5]
#   for water areas the overlay works and slices the right sized area from whole data. open data as geodtaaframe

coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.))
polygon = Polygon(coords)
area = gpd.GeoSeries(polygon)
bbox = gpd.GeoDataFrame({'geometry': area})
bbox = bbox.set_crs(3067, allow_override=True)

# filepath to open height model from puhti
"""
fp_dem = '/appl/data/geo'
fp_sea = '/appl/data/geo'
fp_lake = '/appl/data/geo'
fp_pointcloud = '/appl/data/geo'
"""

##### open all dems and check whether they are inside the polygon

rasters_included = []

with rasterio.open('fp_dem') as src:
    x = src.transform[2]
    y = src.transform[5]
    print(x)
    print(y)
    coords = ((x, y), (x + 6000, y), (x + 6000, y - 6000), (x, y - 6000))
    dem_area = Polygon(coords)
    area = gpd.GeoSeries(dem_area)
    raster_area = gpd.GeoDataFrame({'geometry': area})
    raster_area2 = bbox.set_crs(3067, allow_override=True)

    if gpd.overlay(raster_area2, bbox,  how='intersection') is not None:
        raster = src.read(1)
        rasters_included. append(raster)

###### selecting certain area from water shapefile ######

sea_data = gpd.read_file('fp')

try:
    raster_area = gpd.overlay(sea_data, bbox,  how='intersection')
    raster_area = gpd.overlay(raster_area, bbox, how='union')
except:
    raster_area = bbox


###### selecting right point clouds ######

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