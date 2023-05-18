#rasterizing classified_points -pointcloud and combining it with elevation model
import numpy as np
import rasterio
import laspy
from rasterio.transform import from_origin
import Visualize_data
from matplotlib import pyplot
from skimage import morphology
from rasterio.windows import Window
import pyproj
import SlicePointcloud


# Rivi = int(index / 30))
#print(int(1 / 30))

arr = np.zeros(shape=(1500,1500)).astype(np.float64)
#print(arr.data)


with rasterio.open('L4131H.tif') as src:

    array = src.read(1)
    print(src.transform[2])
    print(src.transform[5])
    pyplot.imshow(array, cmap='pink')
    pyplot.show()
    # The size in pixels of your desired window
    xsize, ysize = 1500, 1500

    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin1, xmax1 = 0, xsize
    ymin1, ymax1 = 0, ysize
    print(xmin1, xmax1, ymin1, ymax1, "image position")
    # Create a Window and calculate the transform from the source dataset
    window1 = Window(xmin1, ymin1, xsize, ysize)
    transform = src.window_transform(window1)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('output1.tif', 'w', **profile) as dst1:
        # Read the data from the window and write it to the output raster
        dst1.write(src.read(window=window1))

    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin2, xmax2 = 1500, xsize + 1500
    ymin2, ymax2 = 0, ysize
    print(xmin1, xmax2, ymin2, ymax2, "image position")
    # Create a Window and calculate the transform from the source dataset
    window2 = Window(xmin2, ymin2, xsize, ysize)
    transform = src.window_transform(window2)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('output2.tif', 'w', **profile) as dst2:
        # Read the data from the window and write it to the output raster
        dst2.write(src.read(window=window2))

    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin3, xmax3 = 0, xsize
    ymin3, ymax3 = 1500, ysize + 1500
    print(xmin3, xmax3, ymin3, ymax3, "image position")
    # Create a Window and calculate the transform from the source dataset
    window3 = Window(xmin3, ymin3, xsize, ysize)
    transform = src.window_transform(window3)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('output3.tif', 'w', **profile) as dst3:
        # Read the data from the window and write it to the output raster
        dst3.write(src.read(window=window3))


    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin4, xmax4 = 1500, xsize + 1500
    ymin4, ymax4 = 1500, ysize + 1500
    print(xmin4, xmax4, ymin4, ymax4, "image position")
    # Create a Window and calculate the transform from the source dataset
    window4 = Window(xmin4, ymin4, xsize, ysize)
    transform = src.window_transform(window1)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('output4.tif', 'w', **profile) as dst4:
        # Read the data from the window and write it to the output raster
        dst4.write(src.read(window=window4))

with rasterio.open('output1.tif') as cropped1:
    array2 = cropped1.read(1)
    pyplot.imshow(array2, cmap='pink')
    pyplot.show()
"""
with rasterio.open('output2.tif') as cropped2:
    array3 = cropped2.read(1)
    pyplot.imshow(array3, cmap='pink')
    pyplot.show()

with rasterio.open('output3.tif') as cropped3:
    array4 = cropped3.read(1)
    pyplot.imshow(array4, cmap='pink')
    pyplot.show()

with rasterio.open('output4.tif') as cropped4:
    array5 = cropped4.read(1)
    pyplot.imshow(array5, cmap='pink')
    pyplot.show()
"""


size = 10000 # the size of each point cloud side

with rasterio.open('output2.tif') as src:
    #print(src.crs)
    input_tif_h = src.read(1)
    print(input_tif_h[1499])
    #print(src.transform)
    #print(src.transform[2])
    #print(src.transform[5])
heigth_raster = np.zeros(shape=(1500, 1500)).astype(np.float64)
zero_raster = np.zeros(shape=(1500, 1500)).astype(np.float64)

row_b = 0
row_d = 1499
while row_d >= 0:
    row_bldg = zero_raster[row_b]
    row_dem = input_tif_h[row_d]
    heigth_raster[row_d] = row_dem + row_bldg
    row_d = row_d - 1
    row_b = row_b + 1
print(heigth_raster)

with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS/Pointcloud_tests/classified_buildings_points.las") as temp:
    print(temp)
    input_las = temp.read()
    print(input_las)
    print('Points from data:', len(input_las.points))
    header = input_las.header
    header.add_crs(crs=pyproj.CRS(proj='utm', zone=35, ellps='WGS84') ,keep_compatibility=True)
    #print(input_las.X)
    buildings = SlicePointcloud.slicePointcloud(2000, input_las)

pyplot.imshow(buildings, cmap='pink')
pyplot.show()



# performing opening and closing to the raster to fill the gaps and remove outliers
opened_raster = morphology.area_opening(buildings, area_threshold=5, connectivity=2)
result_raster = morphology.area_closing(opened_raster, area_threshold=8, connectivity=2)

pyplot.imshow(result_raster, cmap='pink')
pyplot.show()

height_raster = input_tif_h + result_raster

pyplot.imshow(height_raster, cmap='pink')
pyplot.show()


transform = from_origin(src.transform[2], src.transform[5], 2, 2)
new_dataset = rasterio.open('height_raster_test.tif', 'w', driver='GTiff',
                            height = height_raster.shape[0], width = height_raster.shape[1],
                            count=1, dtype=str(height_raster.dtype),
                            transform=transform)

new_dataset.write(height_raster, 1)
new_dataset.close()

#point_data = np.stack([input_las.X, input_las.Y, input_las.Z], axis=0).transpose((1, 0))


"""
    
def rasterize(pcd, size, n):
    # n defines th index in pcd list and thus defines the X, Y, end_X and end_Y

    px = int(size / 200)

    X = (n % 30) * size
    end_X = X + 200
    Y = int(n / 30) * size
    end_Y = Y + 200

    buildings = np.zeros(shape=(px, px)).astype(np.float64)

    y = 49
    x = 0
    print(X, Y)
    while y >= 0:
        while x < 50:
            points_in_pixel = []
            for point in pcd:
                # (point[0], point[1], point[2])

                if X < point[0] < end_X and Y < point[1] < end_Y:
                    print(point[2])
                    points_in_pixel.append(point[2])
                    if len(points_in_pixel) > 1:
                        sum = 0
                        count = 0
                        for p in points_in_pixel:
                            sum += p
                            count += 1
                        h = sum / count
                        buildings[x][y] = h
                        print(buildings[x][y], "height many")
                    elif len(points_in_pixel) == 1:
                        h = points_in_pixel[0]
                        buildings[x][y] = h
                        print(buildings[x][y], "height 1")
            x = x + 1
            X = X + 200
            end_X = end_X + 200

        y = y - 1
        Y = Y + 200
        end_Y = end_Y + 200

    return buildings
    buildings = np.zeros(shape=(1500, 1500)).astype(np.float64)
    #print(arr)
    X_r = 0 #starting pixel in raster i  X direction
    Y_r = 0 #starting pixel in raster in Y direction
    pcd_side_x = 50 # size of the side of the point cloud in pixels
    pcd_side_y = 50 # size of the side of the point cloud in pixels
    count = 0 #Counter to keep in track the list index
    pcd = sliced_pcds[count]
    X = 0
    end_X = X + 200
    Y = 0
    end_Y = Y + 200

    while count < 900: # number of list indexes is 900
        Y_r = 0
        while Y_r < pcd_side_y:

            column = buildings[Y_r]
            #print(pcd)

            if 900 % (count + 1) == 0:
                X_r = 0
                pcd_side_x = 50

            while X_r < pcd_side_x:
                #go through the first list in sliced_pcd
                points_in_pixel = []
                height = column[X_r]
                for point in pcd:

                    # if point is in 2 x 2 area it is considered as a height of that pixel
                    # (point[0], point[1], point[2])
                    if X < point[0] < end_X and Y > point[1] > end_Y:
                        print(point[2])
                        points_in_pixel.append(point[2])
                        if len(points_in_pixel) > 1:
                            sum = 0
                            count_2 = 0
                            for p in points_in_pixel:
                                sum += p
                                count_2 += 1
                            h = sum / count_2

                        elif len(points_in_pixel) == 1:
                            h = points_in_pixel[0]
                            height = h


                X = X + 200 #increasing the point cloud index
                end_X = end_X + 200

                X_r = X_r + 1

            X_r = 0
            X = X + 200  # Increasing the point cloud index
            end_X = end_X + 200
            Y_r = Y_r + 1
            
        X_r = X_r + 50
        pcd_side_x = pcd_side_x + 50
        count = count + 1
        pcd = sliced_pcds[count]

    print(buildings)



    
    for row in buildings:
        for height in row:
            points_in_pixel = []
            for point in point_data:
                #(point[0], point[1], point[2])
                if X < point[0] < end_X and Y < point[1] < end_Y:
                    print(point[2])
                    points_in_pixel.append(point[2])
                    if len(points_in_pixel) > 1:
                        sum = 0
                        count = 0
                        for p in points_in_pixel:
                            sum += p
                            count += 1
                        h = sum / count
                        height = h
                    elif len(points_in_pixel) == 1:
                        h = points_in_pixel[0]
                        height = h
            X = X + 200
            end_X = end_X + 200
            Y = Y + 200
            end_Y = end_Y + 200
            
    print(buildings)
"""



#Visualize_data.visualize_data(point_data)


