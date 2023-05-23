import numpy as np
import laspy
import Classify_buildings
import Visualize_data

with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS-project/Input data/Pointcloud/leppävaara.laz") as temp:
    print(temp)
    input_las = temp.read()
    print(input_las)
    print('Points from data:', len(input_las.points))
    ground_pts = input_las.classification == 2
    bins, counts = np.unique(input_las.return_number[ground_pts], return_counts=True)
    print('Ground Point Return Number distribution:')
    for r, c in zip(bins, counts):
        print('    {}:{}'.format(r, c))

point_format = input_las.point_format

print(point_format.id)

print(list(point_format.dimension_names))

point_data = np.stack([input_las.X, input_las.Y, input_las.Z], axis=0).transpose((1, 0))
print(point_data)

Visualize_data.visualize_data(point_data)
not_ground = laspy.create(point_format=input_las.header.point_format, file_version=input_las.header.version)
not_ground.points = input_las.points[input_las.classification != 2]
not_ground.points = input_las.points[input_las.number_of_returns == 2]
data = np.stack([not_ground.X, not_ground.Y, not_ground.Z], axis=0).transpose((1, 0))

buildings = laspy.create(point_format=input_las.header.point_format, file_version=input_las.header.version)
buildings.points = input_las.points[input_las.return_number == 1]

buildings.points = buildings.points[buildings.number_of_returns == 1]
buildings.points = buildings.points[buildings.classification == 5]

buildings_data = np.stack([buildings.X, buildings.Y, buildings.Z], axis=0).transpose((1, 0))

#Visualize whole data

#Classify buldings points with 10 closest points
classified_points = Classify_buildings.Classify(buildings_data, 10)
print(classified_points)

classified_buildings = np.stack(classified_points)
Visualize_data.visualize_data(classified_buildings)

header = laspy.LasHeader(point_format=3, version="1.2")
header.offsets = np.min(classified_buildings, axis=0)
header.scales = np.array([0.1, 0.1, 0.1])

# 3. Create a LasWriter and a point record, then write it
with laspy.open("classified_buildings_points.las", mode="w", header=header) as writer:
    point_record2 = laspy.ScaleAwarePointRecord.zeros(classified_buildings.shape[0], header=header)
    print(classified_buildings)
    point_record2.x = classified_buildings[:, 0]
    point_record2.y = classified_buildings[:, 1]
    point_record2.z = classified_buildings[:, 2]

    writer.write_points(point_record2)
    print("success !")