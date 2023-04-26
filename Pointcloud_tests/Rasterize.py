#rasterizing classified_points -pointcloud and combining it with elevation model
import numpy as np
import rasterio
import laspy
from rasterio.transform import from_origin
import Visualize_data

arr = np.zeros(shape=(1500,1500)).astype(np.float64)
print(arr)

transform = from_origin(472137, 5015782, 2, 2)

new_dataset = rasterio.open('test1.tif', 'w', driver='GTiff',
                            height = arr.shape[0], width = arr.shape[1],
                            count=1, dtype=str(arr.dtype),
                            crs='+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs',
                            transform=transform)

with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS/Pointcloud_tests/classified_buildings_points.las") as temp:
    print(temp)
    input_las = temp.read()
    print(input_las)
    print('Points from data:', len(input_las.points))

point_data = np.stack([input_las.X, input_las.Y, input_las.Z], axis=0).transpose((1, 0))
Visualize_data.visualize_data(point_data)

new_dataset.write(arr, 1)
print(arr)
new_dataset.close()