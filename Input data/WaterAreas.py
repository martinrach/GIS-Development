import geopandas as gpd
import matplotlib.pyplot as plt
from geocube.api.core import make_geocube
import rasterio

from shapely.geometry import Polygon


# File path
#fp1 = "WaterAreas/jarvi10.shp"
fp2 = "WaterAreas/meri10.shp"
fp3 = "WaterAreas/jokiAlue10.shp"

#lake_data = gpd.read_file(fp1)
sea_data = gpd.read_file(fp2)
river_data = gpd.read_file(fp3)
print(sea_data)

# pick only certain area of the data frame
# Create mas covering the area wanted
# get parameters from the dem transform[2] and transform[5]
x = 377000
y = 6678000
x_end =  380000
y_end =  6675000

area = gpd.GeoSeries(Polygon([(x,y_end), (x, y), (x_end, y), (x_end, y_end)]))
bbox = gpd.GeoDataFrame({'geometry': area})
bbox = bbox.set_crs(3067, allow_override=True)
print(bbox)

try:
    raster_area = gpd.overlay(sea_data, bbox,  how='intersection')
    raster_area = gpd.overlay(raster_area, bbox, how='union')
except:
    raster_area = bbox

"""
try:
    raster_area2 = gpd.overlay(lake_data, bbox,  how='intersection')
    raster_area2 = gpd.overlay(raster_area2, bbox, how='union')
except:
    raster_area2 = bbox


try:
    raster_area3 = gpd.overlay(river_data, bbox,  how='intersection')
    raster_area3 = gpd.overlay(raster_area3, bbox, how='union')
except:
    raster_area3 = bbox
"""

print(raster_area)

# Using GeoCube to rasterize the Vector
sea_raster = make_geocube(
    vector_data=raster_area,
    resolution=(-2, 2),
    fill= 0
)
"""
lake_raster = make_geocube(
    vector_data=raster_area2,
    resolution=(-2, 2),
    fill= 0
)


river_raster = make_geocube(
    vector_data=raster_area3,
    resolution=(-2, 2),
    fill= 0
)
"""
# Save raster census raster
sea_raster.rio.to_raster('test_sea_raster.tif')
#lake_raster.rio.to_raster('test_lake_raster.tif')
#river_raster.rio.to_raster('test_river_raster.tif')

with rasterio.open('test_sea_raster.tif') as src:
    raster = src.read(1)

plt.imshow(raster)
plt.show()


